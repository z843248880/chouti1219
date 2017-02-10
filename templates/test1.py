
import json

# dic = {
#     "(1     qqq    None)":{
#         "(2     360    1)": {
#             "(4     baidu  2)": {}
#         },
#         "(3     ali    1)": {}
#     },
#     "(5     baidu  None)": {
#         "(8     baidu  5)": {}
#     },
#     "(6     baidu  None)": {
#         "(7     baidu  6)": {}
#     }
# }
#
#
# dic1 = {
#
# }
# dic1['(1     qqq    None)'] = 2
#
# for k,v in dic1.items():
#     print(k,v)
#
#
# a = json.dumps(dic)
# print(a)

import collections

dic = {
    "(1,qqq,None)":{
        "(2,360,1)": {
            "(4,baidu,2)": {}
        },
        "(3,ali,1)": {}
    },
    "(5,baidu,None)": {
        "(8,baidu,5)": {}
    },
    "(6,baidu,None)": {
        "(7,baidu,6)": {}
    }
}

a = json.dumps(dic)
b = json.loads(a)
for k,v in b.items():
    print(k,v)

import time
print(time.time())









def tree_search(d_dic, comment_obj):
    for k, v_dic in d_dic.items():
        # print(k)
        # print('----------------: ',str(k[0]),'  &  ',comment_obj[5])
        if str(k.strip('()').split(',')[0]) == comment_obj[5]:
            d_dic[k][str(comment_obj)] = collections.OrderedDict()
            return
        else:
            if v_dic:
                tree_search(d_dic[k], comment_obj)


def build_tree(comment_list):
    comment_dic = collections.OrderedDict()
    for comment_obj in comment_list:
        # print('funck?:',type(str(comment_obj[5])),'_________-',comment_obj[5])
        if str(comment_obj[5]) == 'None':
            comment_dic[str(comment_obj)] = collections.OrderedDict()
        else:
            tree_search(comment_dic, comment_obj)
    return comment_dic
















html_str = '';
        marg = 0;
        digui_count = 0;
        function ccitest(tessta,newsnid) {
            for(var key in tessta){
                var key_list = key.substring(1,key.length - 1).split(',');
                var username = key_list[2];
                var contentneirongold = key_list[1];
                var contentneirong = contentneirongold.replaceAll(contentneirongold,"'","").trim();
                var contenttimeold = key_list[4] + key_list[5] + key_list[6] + key_list[7] + key_list[8] + key_list[9];
                var contenttime = contenttimeold.substring(18,key.length);
                var contentid = key_list[0];
        {#                var biaozhi = '19';#}
                var biaozhi = key_list[10];
                var newbiaozhi = biaozhi.replaceAll(biaozhi,"'","").trim();
                if(newbiaozhi == 'None'){
                    marg = 0;
                    html_str += '<li class="content-li-list" style="border-top: 1px grey dashed;">' + '<div class="content-li-list-area" onmouseover="displayCommentReply(this);" onmouseout="hideCommentReply(this);" ' + 'style="margin-left:' + marg + 'px;">' + '<a class=content-user style="color: #369;">' + username + '</a>' + '     ' + '<span class="content-neirong" style="font-size: 14px;">' + contentneirong + '     ' + contenttime + '发布' + '</span>' + '<a class="comment-reply hide" onclick="replyComment(this,' + username +',' + newsnid +');">       回复</a>' + '<i class="contentidi hide">' + contentid + '</i>' + '</div> </li>';
                }else{
                    marg += 30;
                    html_str += '<li class="content-li-list">' + '<div class="content-li-list-area" onmouseover="displayCommentReply(this);" onmouseout="hideCommentReply(this);" ' + 'style="margin-left:' + marg + 'px;">' + '<a class=content-user style="color: #369;">' + username + '</a>' + '     ' + '<span class="content-neirong" style="font-size: 14px;">' + contentneirong + '     ' + contenttime + '发布' + '</span>' + '<a class="comment-reply hide" onclick="replyComment(this,' + username +',' + newsnid +');">       回复</a>' + '<i class="contentidi hide">' + contentid + '</i>' + '</div> </li>';
                }
                var testret = testdictnull(tessta[key]);
                if(testret){
                    console.log('1');
                    ccitest(tessta[key],newsnid);
                }else{
                    console.log('2');

{#                    if(marg > 30){#}
{#                        marg -= 30 * digui_count;#}
{#                        digui_count = 0;#}
{#                    }#}

{#                    ccitest(tessta[key],newsnid);#}
                }
            }
            return html_str
        }

        marg = 30

        function testdictnull(dict) {
            for(var key in dict){
                return true;
            }
            return false;
        }














