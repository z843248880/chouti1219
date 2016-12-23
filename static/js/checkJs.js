/**
 * Created by root on 12/22/16.
 */
(function(jq){


    function ErrorMessage(inp,message){
        var tag = document.createElement('span');
        tag.innerText = message;
        inp.after(tag);
    }

    jq.extend({
        valid:function(form){
            jq('.btn-login-span').click(function(){
                var flag = true;
                jq(form).find('span').remove();
                jq(form).find(':text,:password').each(function(){
                    var requireStatus = $(this).attr('require');
                    if(requireStatus){


                        var val = $(this).val();
                        if(val.length<=0){
                            var label = $(this).attr('label');
                            ErrorMessage($(this),label + '不能为空');
                            flag = false;


                            return false;

                        }





                        var minLen=$(this).attr('minLen');
                        var intMinLen = parseInt(minLen);
                        if(val.length<=intMinLen){
                            var label = $(this).attr('label');
                            ErrorMessage($(this),label + '不能小于' + minLen);
                            flag = false;
                            return false;

                        }


                        var phoneStatus = $(this).attr('phone');


                        var phoneReg = /^1[3|5|7|8]\d{9}$/
                        if(phoneStatus){
                            if(!phoneReg.test(val)){
                                var label = $(this).attr('label');
                                ErrorMessage($(this),label + '格式错误');
                                flag = false;
                                return false;

                            }

                        }


                    }
                });

                return flag;
            });
        }
    });
})(jQuery);