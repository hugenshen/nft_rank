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
def rareRank(all_NFT):

    jd_means=[]
    #计算所有的JD
    for i,each_NFT in enumerate(all_NFT):
        jd_results = []
        for other_NFT in all_NFT[0:i]+all_NFT[i+1:]:
            jd_results.append(jaccardDistance(each_NFT,other_NFT))
        jd_means.append(np.mean(jd_results))

    #平均值作为当前NFT的初始稀有度,放在集合最后一个
    jd_means=np.array(jd_means)
    #z-score归一化
    jd_zscore=(jd_means-jd_means.min())/(jd_means.max()-jd_means.min())
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
