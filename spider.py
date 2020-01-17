# -*- coding: utf-8 -*-
import datetime
import os
import requests
import pandas as pd
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

cities = {'安吉': 686, '安图': 643, '安庆': 179, '安康': 545, '安阳': 412, '安顺': 518, '澳门': 39, '阿克苏': 920, '阿勒泰': 427, '阿坝': 744, '阿尔山': 120084, '阿拉善': 1193, '阿里': 99, '鞍山': 229, '亳州': 404, '保亭': 1009, '保定': 459, '保山': 420, '包头': 347, '北京': 1, '北戴河': 1938, '北海': 140, '博尔塔拉': 2513, '宝鸡': 422, '巴中': 703, '巴彦淖尔': 883, '巴音郭楞': 2512, '巴马': 3041, '布尔津': 1010, '本溪': 463, '毕节': 521, '滨州': 660, '白城': 870, '白山': 871, '白银': 828, '百色': 524, '蚌埠': 205, '从化区': 621, '崇州': 909, '崇左': 837, '崇礼区': 2548, '常州': 206, '常德': 417, '常熟': 101, '慈溪': 543, '成都': 104, '承德': 135, '昌吉': 923, '昌江': 2456, '昌都': 559, '朝阳': 1104, '楚雄': 510, '池州': 825, '沧州': 540, '淳安': 2249, '滁州': 228, '潮州': 467, '澄迈': 2457, '赤峰': 483, '郴州': 336, '重庆': 158, '长岛': 505, '长春': 216, '长沙': 148, '长治': 901, '长白山': 268, '东莞': 212, '东营': 612, '东阳': 608, '丹东': 315, '丹巴': 704, '儋州': 841, '大兴安岭': 396, '大同': 275, '大庆': 531, '大理': 31, '大连': 4, '大邑': 3130, '定安': 2021, '定西': 830, '德宏': 526, '德州': 603, '德清': 1011, '德阳': 462, '敦化': 1388, '敦煌': 8, '登封': 1014, '稻城': 342, '达州': 910, '迪庆': 120009, '都江堰': 911, '峨眉山': 24, '恩施': 487, '鄂尔多斯': 600, '鄂州': 858, '佛山': 207, '凤凰': 988, '奉化区': 1020, '抚州': 875, '抚顺': 514, '福州': 164, '福鼎': 613, '阜新': 879, '阜阳': 361, '防城港': 698, '固原': 888, '广元': 593, '广安': 693, '广州': 152, '广汉': 1349, '果洛': 120013, '桂林': 28, '甘南': 426, '甘孜': 754, '贵港': 711, '贵阳': 33, '赣州': 473, '高雄': 756, '华山': 183, '华阴': 476, '合肥': 196, '呼伦贝尔': 458, '呼和浩特': 156, '和田': 557, '哈密市': 567, '哈尔滨': 151, '怀化': 655, '惠东': 956, '惠州': 213, '杭州': 14, '横店影视城': 1096, '汉中': 486, '河池': 838, '河源': 350, '海东': 120010, '海北': 120014, '海口': 37, '海螺沟': 705, '海西': 120012, '海阳': 1188, '淮北': 657, '淮南': 638, '淮安': 351, '湖州': 68, '红原': 3099, '红河': 512, '花莲': 1366, '菏泽': 708, '葫芦岛': 345, '衡山': 277, '衡水': 461, '衡阳': 864, '贺州': 707, '邯郸': 495, '香港': 38, '鹤壁': 595, '鹤岗': 811, '黄冈': 859, '黄南': 120042, '黄山': 120061, '黄果树': 143874, '黄石': 710, '黑河': 265, '九华山': 182, '九寨沟': 25, '九江': 877, '井冈山': 171, '佳木斯': 501, '即墨区': 1532, '吉安': 876, '吉林市': 267, '嘉义市': 758, '嘉兴': 272, '嘉善': 1019, '嘉峪关': 284, '基隆': 1382, '建水': 2151, '揭阳': 835, '晋中': 639, '晋城': 665, '景德镇': 405, '景洪': 2154, '江门': 362, '济南': 128, '济宁': 658, '济源': 640, '焦作': 663, '绩溪': 2627, '荆州': 413, '荆门': 634, '酒泉': 282, '金华': 219, '金昌': 832, '金门': 1368, '锦州': 513, '靖西': 967, '鸡西': 852, '克什克腾旗': 2971, '克孜勒苏': 2511, '克拉玛依': 428, '凯里': 491, '喀什': 124, '喀纳斯': 816, '康定': 344, '开封': 165, '开平': 525, '昆山': 77, '昆明': 29, '临夏': 833, '临安区': 88, '临汾': 318, '临沂': 480, '临沧': 926, '临高': 2458, '丽水': 441, '丽江': 32, '乐东': 981, '乐山': 103, '六安': 502, '六盘水': 679, '兰州': 231, '凉山': 912, '利川': 984, '吕梁': 902, '娄底': 866, '庐山风景区': 20, '廊坊': 582, '拉萨': 36, '来宾': 839, '林芝': 126, '柳州': 143, '泸州': 604, '洛阳': 198, '浏阳': 1337, '溧阳': 598, '漯河': 664, '聊城': 635, '荔波': 659, '莱芜区': 794, '辽源': 872, '辽阳': 881, '连云港': 238, '连城': 609, '陇南': 1491, '陵水': 1509, '雷山': 2345, '黎平': 1346, '龙岩': 366, '龙虎山': 160, '弥勒': 1342, '梅州': 523, '满洲里': 319, '漠河': 983, '牡丹江': 264, '眉山': 914, '绵阳': 915, '芒市': 2199, '苗栗': 3199, '茂名': 615, '马鞍山': 503, '内江': 823, '南京': 9, '南充': 782, '南宁': 166, '南平': 827, '南投市': 759, '南昌': 175, '南浔古镇': 80, '南通': 85, '南阳': 591, '南靖': 2672, '宁德': 490, '宁波': 83, '宁海': 689, '宁蒗': 2169, '怒江': 681, '那曲': 919, '屏东': 1364, '平凉': 424, '平遥': 365, '平顶山': 810, '攀枝花': 786, '普洱': 928, '普陀山': 16, '澎湖': 1367, '濮阳': 581, '盘锦': 602, '莆田': 317, '萍乡': 714, '蓬莱': 168, '七台河': 1179, '千岛湖': 17, '庆阳': 834, '曲阜': 129, '曲靖': 509, '泉州': 243, '清远': 517, '琼海': 843, '秦皇岛': 132, '衢州': 174, '钦州': 697, '青岛': 5, '黔东南': 2375, '黔南': 2374, '黔西南': 1428, '齐齐哈尔': 395, '日喀则': 100, '日照': 622, '若尔盖': 3165, '三亚': 61, '三明': 620, '三清山': 159, '三门峡': 522, '上海': 2, '上饶': 547, '十堰': 464, '双鸭山': 854, '商丘': 849, '商洛': 906, '四平': 556, '宿州': 672, '宿迁': 492, '山南': 339, '朔州': 903, '松原': 873, '汕头': 215, '汕尾': 624, '沈阳': 155, '深圳': 26, '石嘴山': 889, '石家庄': 199, '石林': 271, '石河子': 1168, '神农架': 147, '绍兴': 18, '绥化': 856, '苏州': 11, '遂宁': 605, '邵阳': 867, '随州': 860, '韶关': 222, '韶山': 346, '台东': 760, '台中': 1369, '台北': 360, '台南': 757, '台山': 673, '台州': 402, '吐鲁番市': 35, '唐山': 200, '塔城': 924, '天水': 285, '天津': 154, '太仓': 255, '太原': 167, '太湖': 2603, '屯昌': 845, '桃园市': 1439, '桐乡': 220, '桐庐': 688, '泰宁': 2678, '泰安': 746, '泰山': 6, '泰州': 494, '腾冲': 696, '通化': 874, '通辽': 885, '铁岭': 589, '铜仁': 680, '铜川': 907, '铜陵': 472, '万宁': 846, '乌兰察布': 1358, '乌镇': 508, '乌鲁木齐': 117, '乌鲁木齐县': 2489, '五台山': 184, '五指山': 982, '吴忠': 890, '威海': 169, '婺源': 446, '文山': 511, '文昌': 1007, '无锡': 10, '梧州': 142, '武义': 1004, '武夷山': 22, '武威': 290, '武当山': 146, '武汉': 145, '武隆区': 120015, '汶川': 3101, '温州': 153, '渭南': 908, '潍坊': 226, '芜湖': 457, '信阳': 448, '兴城': 1399, '兴安盟': 886, '厦门': 21, '咸宁': 861, '咸阳': 632, '孝感': 862, '宣城': 504, '徐州': 230, '忻州': 783, '新乡': 474, '新余': 878, '新北': 2063, '新竹': 1197, '湘潭': 1417, '湘西': 496, '襄阳': 414, '西双版纳': 30, '西塘': 15, '西宁': 237, '西安': 7, '西昌': 592, '许昌': 465, '象山': 723, '邢台': 460, '锡林郭勒盟': 484, '雪乡': 1445063, '香格里拉': 106, '义乌': 1005, '云林县': 3197, '云浮': 836, '亚布力滑雪旅游度假区': 815, '伊宁市': 2058, '伊春': 498, '伊犁': 115, '宜兰': 1383, '宜兴': 227, '宜宾': 278, '宜昌': 313, '宜春': 743, '岳阳': 287, '延吉': 475, '延安': 423, '延边': 415, '扬州': 12, '榆林': 485, '永州': 869, '烟台': 170, '玉林': 141, '玉树': 896, '玉溪': 477, '益阳': 868, '盐城': 493, '营口': 692, '运城': 397, '银川': 239, '阳朔': 702, '阳江': 363, '阳泉': 904, '雅安': 917, '鹰潭': 186, '中卫': 1184, '中山': 233, '周口': 709, '周庄': 81, '张家口': 497, '张家界': 23, '张掖': 283, '彰化': 3180, '昭通': 929, '枣庄': 656, '株洲': 1174, '淄博': 536, '湛江': 202, '漳州': 334, '珠海': 27, '肇庆': 269, '自贡': 575, '舟山': 479, '资阳': 918, '遵义': 204, '郑州': 157, '镇江': 13, '镇远': 1840, '驻马店': 642}


def city_spider():
    city_url = 'http://sec-m.ctrip.com/restapi/soa2/12530/json/cityList?_fxpcqlniredt=09031150411707933324'
    data = {"pageid": 214422, "limit": 10000, "source": 0, "type": 0, "contentType": "json",
            "head": {"cid": "09031150411707933324", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                     "syscode": "09", "auth": "", "extension": [{"name": "protocal", "value": "https"}]},
            "ver": "7.14.2"}
    header = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': '_abtest_userid=8401d222-6177-4e40-8d08-149366abd9c8; _RF1=115.238.47.230; _RGUID=001df58f-2b4a-4b03-b813-4ed1662715f7; _RDG=286f5d405adf8f2126286fae667fc0dbd0; _RSG=3iaIhyOzT00tNn9c5jJJWB; MKT_CKID_LMT=1579158186298; MKT_CKID=1579158186297.rtqrs.8ar4; _gid=GA1.2.1936271753.1579158187; _ga=GA1.2.1466164872.1579158187; gad_city=78a2062d1790b42fa1a75f591a7869b2; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; StartCity_Pkg=PkgStartCity=1; manualclose=1; GUID=09031150411707933324; MKT_Pagesource=H5; _bfs=1.13; _jzqco=%7C%7C%7C%7C%7C1.349465944.1579158186294.1579161202818.1579163580369.1579161202818.1579163580369.0.0.0.9.9; __zpspc=9.3.1579163580.1579163580.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _bfi=p1%3D103047%26p2%3D600000435%26v1%3D19%26v2%3D18; cticket=6E0B7E1069D610640472C6E9B6989365F58C0D0A3C4FF0341C1EC4FF57045C4F; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yoj538guJumHPPjdpX6KYmBtaD3ZBC/yyyixcTyOC4Mfh1g3EsM0qGrfO7v43vSteasJVWkibf6uWviuN7iHYUV6qtdGxbm2viGnfpuT707HRD6kC497BS8nYpT3CnkJyGlv1PL2OzkS1PLCAJl9TfUJ9JXZFX7dw9w3OvXsqOqxiuQYkiYXFHax7YbH6gYEozcX35u0l89MxVMq/4d8u9vz8zW+Mx5lDc70rEwQ6HNuyyVxP2Wf1Ss3q0xWdgLOoxoRnokOuIitbs=; DUID=u=9AC67314D2045125FF2F77C8F0CD03AC&v=0; IsNonUser=T; Union=OUID=&AllianceID=4897&SID=353693&SourceID=55551825&AppID=&OpenID=&createtime=1579163915&Expires=1579768715097; _bfa=1.1579158183499.2nvhzb.1.1579158183499.1579164127399.3.44.104801; _gat=1',
        'cookieorigin': 'https://m.ctrip.com',
        'origin': 'https://m.ctrip.com',
        'user-agent': ua.random
    }
    ret = requests.post(url=city_url, headers=header, json=data).json()
    cities = ret['data']['domesticcity']['cities']
    need_list = []
    for city in cities:
        need = city['cities']
        need_list += need
    return need_list


def scenery_spider_total(districtid):
    scenery_url = 'http://sec-m.ctrip.com/restapi/soa2/12530/json/ticketSpotSearch?_fxpcqlniredt=09031150411707933324'
    data = {"pageid": 10320662472, "searchtype": 1, "districtid": districtid, "needfact": False, "sort": 1, "pidx": 2,
            "isintion": True, "psize": 20, "imagesize": "C_230_260", "reltype": 7,
            "assistfilter": {"userChooseSite": "1", "userLocationCity": "2",
                             "userLocation": "121.48789949:31.24916171"}, "spara": "", "filters": [], "excepts": [],
            "abtests": [],
            "extendAssociation": [{"key": "srhtraceid", "value": "81073084-3d45-e1ee-0b64-157846890435"}],
            "contentType": "json",
            "head": {"cid": "09031150411707933324", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                     "syscode": "09", "auth": "", "extension": [{"name": "protocal", "value": "https"}]},
            "ver": "7.14.2"}
    header = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': '_abtest_userid=8401d222-6177-4e40-8d08-149366abd9c8; _RF1=115.238.47.230; _RGUID=001df58f-2b4a-4b03-b813-4ed1662715f7; _RDG=286f5d405adf8f2126286fae667fc0dbd0; _RSG=3iaIhyOzT00tNn9c5jJJWB; MKT_CKID_LMT=1579158186298; MKT_CKID=1579158186297.rtqrs.8ar4; _gid=GA1.2.1936271753.1579158187; _ga=GA1.2.1466164872.1579158187; gad_city=78a2062d1790b42fa1a75f591a7869b2; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; StartCity_Pkg=PkgStartCity=1; manualclose=1; GUID=09031150411707933324; MKT_Pagesource=H5; _bfs=1.13; _jzqco=%7C%7C%7C%7C%7C1.349465944.1579158186294.1579161202818.1579163580369.1579161202818.1579163580369.0.0.0.9.9; __zpspc=9.3.1579163580.1579163580.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _bfi=p1%3D103047%26p2%3D600000435%26v1%3D19%26v2%3D18; cticket=6E0B7E1069D610640472C6E9B6989365F58C0D0A3C4FF0341C1EC4FF57045C4F; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yoj538guJumHPPjdpX6KYmBtaD3ZBC/yyyixcTyOC4Mfh1g3EsM0qGrfO7v43vSteasJVWkibf6uWviuN7iHYUV6qtdGxbm2viGnfpuT707HRD6kC497BS8nYpT3CnkJyGlv1PL2OzkS1PLCAJl9TfUJ9JXZFX7dw9w3OvXsqOqxiuQYkiYXFHax7YbH6gYEozcX35u0l89MxVMq/4d8u9vz8zW+Mx5lDc70rEwQ6HNuyyVxP2Wf1Ss3q0xWdgLOoxoRnokOuIitbs=; DUID=u=9AC67314D2045125FF2F77C8F0CD03AC&v=0; IsNonUser=T; Union=OUID=&AllianceID=4897&SID=353693&SourceID=55551825&AppID=&OpenID=&createtime=1579163915&Expires=1579768715097; _bfa=1.1579158183499.2nvhzb.1.1579158183499.1579164127399.3.44.104801; _gat=1',
        'cookieorigin': 'https://m.ctrip.com',
        'origin': 'https://m.ctrip.com',
        'user-agent': ua.random
    }
    ret = requests.post(url=scenery_url, headers=header, json=data).json()
    total = ret['data']['total']
    viewspots = ret['data']['viewspots']
    name_list = []
    for viewspot in viewspots:
        name = viewspot['name']
        name_list.append(name)
    return total


def scenery_spider(districtid, page):
    scenery_url = 'http://sec-m.ctrip.com/restapi/soa2/12530/json/ticketSpotSearch?_fxpcqlniredt=09031150411707933324'
    data = {"pageid": 10320662472, "searchtype": 1, "districtid": districtid, "needfact": False, "sort": 1, "pidx": page,
            "isintion": True, "psize": 20, "imagesize": "C_230_260", "reltype": 7,
            "assistfilter": {"userChooseSite": "1", "userLocationCity": "2",
                             "userLocation": "121.48789949:31.24916171"}, "spara": "", "filters": [], "excepts": [],
            "abtests": [],
            "extendAssociation": [{"key": "srhtraceid", "value": "81073084-3d45-e1ee-0b64-157846890435"}],
            "contentType": "json",
            "head": {"cid": "09031150411707933324", "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888",
                     "syscode": "09", "auth": "", "extension": [{"name": "protocal", "value": "https"}]},
            "ver": "7.14.2"}
    header = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': '_abtest_userid=8401d222-6177-4e40-8d08-149366abd9c8; _RF1=115.238.47.230; _RGUID=001df58f-2b4a-4b03-b813-4ed1662715f7; _RDG=286f5d405adf8f2126286fae667fc0dbd0; _RSG=3iaIhyOzT00tNn9c5jJJWB; MKT_CKID_LMT=1579158186298; MKT_CKID=1579158186297.rtqrs.8ar4; _gid=GA1.2.1936271753.1579158187; _ga=GA1.2.1466164872.1579158187; gad_city=78a2062d1790b42fa1a75f591a7869b2; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; StartCity_Pkg=PkgStartCity=1; manualclose=1; GUID=09031150411707933324; MKT_Pagesource=H5; _bfs=1.13; _jzqco=%7C%7C%7C%7C%7C1.349465944.1579158186294.1579161202818.1579163580369.1579161202818.1579163580369.0.0.0.9.9; __zpspc=9.3.1579163580.1579163580.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _bfi=p1%3D103047%26p2%3D600000435%26v1%3D19%26v2%3D18; cticket=6E0B7E1069D610640472C6E9B6989365F58C0D0A3C4FF0341C1EC4FF57045C4F; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yoj538guJumHPPjdpX6KYmBtaD3ZBC/yyyixcTyOC4Mfh1g3EsM0qGrfO7v43vSteasJVWkibf6uWviuN7iHYUV6qtdGxbm2viGnfpuT707HRD6kC497BS8nYpT3CnkJyGlv1PL2OzkS1PLCAJl9TfUJ9JXZFX7dw9w3OvXsqOqxiuQYkiYXFHax7YbH6gYEozcX35u0l89MxVMq/4d8u9vz8zW+Mx5lDc70rEwQ6HNuyyVxP2Wf1Ss3q0xWdgLOoxoRnokOuIitbs=; DUID=u=9AC67314D2045125FF2F77C8F0CD03AC&v=0; IsNonUser=T; Union=OUID=&AllianceID=4897&SID=353693&SourceID=55551825&AppID=&OpenID=&createtime=1579163915&Expires=1579768715097; _bfa=1.1579158183499.2nvhzb.1.1579158183499.1579164127399.3.44.104801; _gat=1',
        'cookieorigin': 'https://m.ctrip.com',
        'origin': 'https://m.ctrip.com',
        'user-agent': ua.random
    }
    ret = requests.post(url=scenery_url, headers=header, json=data).json()
    viewspots = ret['data']['viewspots']
    name_list = []
    for viewspot in viewspots:
        name = viewspot['name']
        name_list.append(name)
    return name_list



def xc_spider(keyword):
    url = 'https://sec-m.ctrip.com/restapi/soa2/10220/json/ActivitySearch?_fxpcqlniredt=09031150411707933324&__gw_appid=99999999&__gw_ver=1.0&__gw_from=0&__gw_platform=H5'

    header = {
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'cookie': '_abtest_userid=8401d222-6177-4e40-8d08-149366abd9c8; _RF1=115.238.47.230; _RGUID=001df58f-2b4a-4b03-b813-4ed1662715f7; _RDG=286f5d405adf8f2126286fae667fc0dbd0; _RSG=3iaIhyOzT00tNn9c5jJJWB; MKT_CKID_LMT=1579158186298; MKT_CKID=1579158186297.rtqrs.8ar4; _gid=GA1.2.1936271753.1579158187; _ga=GA1.2.1466164872.1579158187; gad_city=78a2062d1790b42fa1a75f591a7869b2; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; StartCity_Pkg=PkgStartCity=1; manualclose=1; GUID=09031150411707933324; MKT_Pagesource=H5; _bfs=1.13; _jzqco=%7C%7C%7C%7C%7C1.349465944.1579158186294.1579161202818.1579163580369.1579161202818.1579163580369.0.0.0.9.9; __zpspc=9.3.1579163580.1579163580.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _bfi=p1%3D103047%26p2%3D600000435%26v1%3D19%26v2%3D18; cticket=6E0B7E1069D610640472C6E9B6989365F58C0D0A3C4FF0341C1EC4FF57045C4F; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yoj538guJumHPPjdpX6KYmBtaD3ZBC/yyyixcTyOC4Mfh1g3EsM0qGrfO7v43vSteasJVWkibf6uWviuN7iHYUV6qtdGxbm2viGnfpuT707HRD6kC497BS8nYpT3CnkJyGlv1PL2OzkS1PLCAJl9TfUJ9JXZFX7dw9w3OvXsqOqxiuQYkiYXFHax7YbH6gYEozcX35u0l89MxVMq/4d8u9vz8zW+Mx5lDc70rEwQ6HNuyyVxP2Wf1Ss3q0xWdgLOoxoRnokOuIitbs=; DUID=u=9AC67314D2045125FF2F77C8F0CD03AC&v=0; IsNonUser=T; Union=OUID=&AllianceID=4897&SID=353693&SourceID=55551825&AppID=&OpenID=&createtime=1579163915&Expires=1579768715097; _bfa=1.1579158183499.2nvhzb.1.1579158183499.1579164127399.3.44.104801; _gat=1',
        'cookieorigin': 'https://m.ctrip.com',
        'origin': 'https://m.ctrip.com',
        'user-agent': ua.random
    }

    data = {"ver": "8.3.2", "debug": False, "pidx": 1, "isFirstScreen": True,
            "abtest": [{"tsource": "optimizedactsearch"}],
            "keyword": keyword,
            "binfos": ["false"], "iscouponpage": False, "promotionids": "", "pshowcode": "audiotour",
            "distids": "", "sort": 1, "psize": 15, "isneedf": True, "gsscid": "2", "gslcid": None, "scenes": 12,
            "lineids": "", "isnumber": False,
            "extras": [{"key": "firstClassId", "value": ""}, {"key": "siteId", "value": "2"},
                       {"key": "idtocode", "value": ""}], "extendtype": 1,
            "traceid": "68716d21-08d4-c7ce-f153-15796f887437", "pageid": 104801,
            "head": {"cid": "09031150411707933324", "ctok": "", "cver": "1.0", "lang": "01", "sid": "55551825",
                     "syscode": "09", "auth": None,
                     "extension": [{"name": "networkstatus", "value": "None"}, {"name": "protocal", "value": "https"}]},
            "contentType": "json"}
    ret = requests.post(url=url, headers=header, json=data).json()
    need_list = []
    activityinfos = ret['data']['activityinfos']
    for activityinfo in activityinfos:
        id = activityinfo['id']
        name = activityinfo['name']  # 名称
        cityname = activityinfo['cityname']  # 城市名称
        mprice = activityinfo['mprice']  # 最贵的价格
        price = activityinfo['price']  # 现在的价格
        saletotal = activityinfo['saletotal']  # 月销量
        avdate = activityinfo['avdate']  # 可用状态
        need_dict = {
            'id': id,
            '语言讲解名称': name,
            '城市': cityname,
            '最高价': mprice,
            '最低价': price,
            '月销量': saletotal,
            '可用状态': avdate,
            '景点': keyword
        }
        need_list.append(need_dict)
    print(need_list)
    return need_list


def save_data(filename, data):
    now = datetime.datetime.now().replace()
    now = str(now)[0:10].replace('-', '').replace(' ', '').replace(':', '')
    if os.path.isfile(filename + str(now) + '.csv'):
        flag = False
    else:
        flag = True
    pd.DataFrame(data).to_csv(filename + str(now) + '.csv', mode='a', index=False, header=flag)


def start(city_name):
    keywords_list = []
    city_id = cities[city_name]
    total = int(scenery_spider_total(city_id))
    print(f'景点总数{total}')
    for page in range(1, total//20+1):
        keywords = scenery_spider(districtid=city_id, page=page)
        print(keywords)
        keywords_list += keywords
    print(f'景点总数{len(keywords_list)}，景点列表{keywords_list}')

    for i in range(0, len(keywords_list)):
        data = xc_spider(keywords_list[i])
        save_data(data=data, filename=city_name)
        print(f'景点总数{len(keywords_list)}，第{i+1}个景点数据存储成功~~~')


if __name__ == '__main__':
    city_name = input("请输入城市名：")
    start(city_name)
