import json
import numpy as np

"""
计算两个NFTJaccard系数,参考:https://en.wikipedia.org/wiki/Jaccard_index

"""
def jaccardDistance(NFT1, NFT2):
    com_traits = len(set(NFT1) & set(NFT2))
    uniq_trains = len(NFT1) + len(NFT2) - com_traits
    return 1 - com_traits / uniq_trains


"""
稀有度 
"""
def rareRank(tar_NFT, all_NFT):
    jd_results = []
    # 计算所有的JD
    for each_NFT in all_NFT:
        jd_results.append(jaccardDistance(tar_NFT, each_NFT))
    # 平均值作为当前NFT的初始稀有度,放在集合最后一个
    jd_results.append(np.mean(jd_results))
    # z-score归一化
    jd_results = np.array(jd_results)
    jd_zscore = (jd_results - jd_results.min()) / (jd_results.max() - jd_results.min())

    return jd_zscore

"""
main方法
"""
if __name__ == '__main__':
    # 此处依赖合约获取nft的attributes,直接读取本地文件进行计算
    nfts_jsons = json.load(open('/Users/hugenshen/Desktop/nft_attributes.json'))
    nfts_attrs = []
    for nfts_json in nfts_jsons:
        nfts_attrs.append([tuple(attr.values()) for attr in nfts_json['attributes']])

    print(np.argsort(rareRank(nfts_attrs[-1], nfts_attrs[:-1])))
