import random
def random_code():
	code = ''
	for i in range(4):
		current = random.randrange(0,4)
		if current != i:
			temp = chr(random.randint(65,90))
		else:
			temp = random.randint(0,9)
		code += str(temp)
	return code.upper()





# {#                whatform1 = 'form-mobilelogin-register';#}
# {#                $('form[class="' + whatform1 + '"] span').not("span[nametag='register-exclude-span']").remove();#}
# {#                code = "";#}
# {#                $('.see-mbck').removeClass('hide');#}
# {#                var codeLength = 4;#}
#         {#            var checkCode = document.getElementById("mbck");#}
# {#                var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',#}
# {#                'S','T','U','V','W','X','Y','Z');#}
# {#                for(var i = 0; i < codeLength; i++) {#}
# {#                    var index = Math.floor(Math.random()*36);#}
# {#                    code += random[index];#}
# {#                }#}
# {#                $('.see-mbck').text(code);#}



# {#                        var coderequire = $(this).attr('coderequire');#}
# {#                        var code_input = $('#mbcd').val();#}
# {#                        if(coderequire){#}
# {#                            if(code != code_input){#}
# {#                                var label = $(this).attr('label');#}
# {#                                ErrorMessage($(this),label + '错误');#}
# {#                                flag = false;#}
# {#                                return false;#}
# {#                            }#}
# {#                        }#}
