from math import floor
import pandas as pd
from collections import defaultdict
import csv
import json
import math
from itertools import combinations as combinations


FILE_PATH = "edit_GR03_contributions.csv"


def round_info():
    df = pd.read_csv(FILE_PATH)
    unique_addresses = df['address'].unique()

    print(f"分析対象のファイル: '{FILE_PATH.split('/')[-1]}'")
    print("ユニークな寄付者数：", "{:,}".format(len(unique_addresses)))
    print("トータルの寄付数：", "{:,}".format(len(df['address'])))


class Grant:
    def __init__(self, grant_id, contributions=None, title=None):
        if contributions is None:
            contributions = []
        self.id = grant_id
        self.contributions = contributions
        self.title = title

    def total_funding(self):
        return sum(self.contributions)

    def match_amount(self, total_match_pool):
        sum_of_sqrts = sum([c**0.5 for c in self.contributions])
        return (sum_of_sqrts**2) * total_match_pool


def calculate_total_match_amounts(grants):
    return sum([grant.match_amount(1) for grant in grants])


def calculate_individual_matches(grants, total_match_pool, total_match_amounts):
    return [grant.match_amount(total_match_pool/total_match_amounts) for grant in grants]


def calculate_contributions(file_path):
    df = pd.read_csv(file_path)
    contributions = defaultdict(list)
    titles = {}
    ids = {}

    for _, row in df.iterrows():
        contributions[row['grant_id']].append(row['amount_in_usdt'])
        titles[row['grant_id']] = row['grant_title']
        ids[row['grant_id']] = row['grant_id']

    return contributions, titles, ids


def calculate_qf_matches(file_path, matching_fund):
    contributions, titles, ids = calculate_contributions(file_path)
    grants = [Grant(ids[grant_id], contributions[grant_id],
                    titles[grant_id]) for grant_id in contributions]
    total_match_amounts = calculate_total_match_amounts(grants)
    matches_qf = calculate_individual_matches(
        grants, matching_fund, total_match_amounts)
    return grants, matches_qf


def クラスタ部分を作る関数():
    # clustered.txtからデータを読み込む
    with open('clustered.txt', 'r') as file:
        clusters = json.load(file)

        # ウォレットアドレスを一意のインデックスにマッピングする
    address_to_index = {}
    index = 0

    # 全てのクラスターとウォレットアドレスをループしてマッピングを作成
    for cluster in clusters:
        for address in cluster:
            if address not in address_to_index:
                address_to_index[address] = index
                index += 1

    # クラスター内のウォレットアドレスをインデックスに変換
    indexed_clusters = []
    for cluster in clusters:
        indexed_cluster = [address_to_index[address] for address in cluster]
        indexed_clusters.append(indexed_cluster)

    return indexed_clusters


indexed_clusters = クラスタ部分を作る関数()


def 寄付部分を作る関数():
    # ファイルパス
    contributions_file_path = '/Users/tkgshn/Downloads/edit_GR03_contributions.csv'

    # プロジェクトIDを格納するためのセット
    project_ids = set()

    # CSVファイルを開いてプロジェクトIDを集計
    with open(contributions_file_path, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            project_ids.add(int(row[1]))  # grant_idは2番目のカラムにある

    # プロジェクトIDをソートしてインデックスを再割り当て
    sorted_project_ids = sorted(list(project_ids))
    project_index = {project_id: index for index,
                     project_id in enumerate(sorted_project_ids)}

    # エージェントごとの寄付を格納するための辞書
    contributions_per_agent = defaultdict(lambda: [0]*len(sorted_project_ids))

    # CSVファイルを開いて寄付を集計
    with open(contributions_file_path, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            agent = row[0]
            project_id = int(row[1])
            contribution = floor(float(row[3]))  # 寄付額は4番目のカラムにある
            # プロジェクトIDを再割り当てしたインデックスに変換
            project_idx = project_index[project_id]
            contributions_per_agent[agent][project_idx] = contribution

    # エージェントごとの寄付リストを作成
    contributions_list = list(contributions_per_agent.values())

    return contributions_list


contributions_list = 寄付部分を作る関数()


def connection_oriented_cluster_match(groups, contributions):
    agents = list(range(len(contributions)))
    if any(any(c < 0 for c in contributions[i]) for i in agents):
        raise NotImplementedError("negative contributions not supported")
    memberships = [len([g for g in groups if i in g]) for i in agents]
    friend_matrix = [[len([g for g in groups if i in g and j in g])
                      for i in agents] for j in agents]
    funding_amounts = []
    for project in range(len(contributions[0])):
        funding_amount = sum(contributions[i][project] for i in agents)
        def K(i, h):
            if sum([friend_matrix[i][j] for j in h]) > 0:
                return math.sqrt(contributions[i][project])
            return contributions[i][project]

        funding_amount += sum(2 * math.sqrt(sum(K(i, p[1])/memberships[i] for i in p[0])) * math.sqrt(
            sum(K(j, p[0])/memberships[j] for j in p[1])) for p in combinations(groups, 2))
        funding_amounts.append(funding_amount)
    return funding_amounts


result = connection_oriented_cluster_match(indexed_clusters, contributions_list)

# プロジェクト名を取得するための関数


def プロジェクト名を取得する関数(contributions_file_path):
    project_names = {}
    with open(contributions_file_path, mode='r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            project_id = int(row[1])
            project_name = row[2]  # 仮にプロジェクト名が3番目のカラムにあるとします
            project_names[project_id] = project_name
    return project_names


# プロジェクト名を取得
contributions_file_path = '/Users/tkgshn/Downloads/edit_GR03_contributions.csv'
project_names = プロジェクト名を取得する関数(contributions_file_path)

# ファンディング額とプロジェクト名を関連付けて最終的な受け取り額を出力する関数


def 最終的な受け取り額を出力する(funding_amounts, project_names, matching_pool):
    total_funding = sum(funding_amounts)
    # sorted_project_ids = sorted(project_names.keys())
    final_amounts = []
    crowdfund_amount_contributions_usd = []

    for i, amount in enumerate(funding_amounts):
        # マッチングプールからの分配額を計算
        distribution_from_pool = matching_pool * (amount / total_funding)
        # 元のファンディング額にマッチングプールからの分配額を加える
        final_get_amount = distribution_from_pool + amount
        final_amounts.append(final_get_amount)
        crowdfund_amount_contributions_usd.append(amount)


    return final_amounts


# マッチングプールの金額を設定
matching_pool = 100000


def calculate_pluralQF():
    plural_qf_results = connection_oriented_cluster_match(
        indexed_clusters, contributions_list)
    project_names = プロジェクト名を取得する関数(FILE_PATH)
    final_amounts = 最終的な受け取り額を出力する(
        plural_qf_results, project_names, matching_pool)
    return final_amounts


def display_results(grants, matches, method):
    total_funding_and_matches = [(grant.title[:30], grant.id, grant.total_funding(
    ), matches[i]) for i, grant in enumerate(grants)]
    total_funding_and_matches.sort(key=lambda x: x[2] + x[3], reverse=True)
    print(f"---------------")
    print(f"{method}を用いた場合（上位15プロジェクトのみ表示中）: ")
    print("{:<30} {:<10} {:<35} {:<15} {:<10} {:<10}".format('grant_title',
          'grant_id', 'crowdfund_amount_contributions_usd', 'Matched_amount_usd', 'total', 'boost(%)'))
    for title, id, total_funding, match in total_funding_and_matches[:15]:
        total = total_funding + match
        boost = ((total - total_funding) / total_funding) * 100  # boostを計算
        print("{:<30} {:<10} {:<35} {:<15} {:<10} {:<10}".format(
            title, id, "{:,.0f}".format(total_funding), "{:,.0f}".format(match), "{:,.0f}".format(total), "{:.0f}%".format(boost)))  # total_funding と match の合計を表示


def main():
    round_info()
    # contributions, titles, ids = calculate_contributions()
    # grants = [Grant(ids[grant_id], contributions[grant_id],
    #                 titles[grant_id]) for grant_id in contributions]
    matching_fund = 100000

    # QFの計算と結果の表示
    grants, matches_qf = calculate_qf_matches(FILE_PATH, matching_fund)
    display_results(grants, matches_qf, "QF")

    # PluralQFの計算と結果の表示
    matches_pluralqf = calculate_pluralQF()
    display_results(grants, matches_pluralqf, "PluralQF")


if __name__ == "__main__":
    main()
