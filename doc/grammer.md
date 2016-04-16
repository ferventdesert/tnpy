> tn是desert和tan共同开发的一种用于匹配，转写和抽取文本的语言。解释器使用Python实现，代码不超过1000行。

本文主要介绍tn的基本语法。高级内容可以参考其他篇章。使用这样的语法，是为了实现语言无关，从而方便地编写不同语言的解释器。

##基本语法
引擎可以由一组规则构成，规则也可以被其他规则所组合。首先介绍最基本的元规则 。 

###1. 字符串StringEntity
```Form1: ("Matched string")
Form2: ("Matched string" : "Rewritten string")
```
Form1是一种省略表达，即Rewritten==Matched
样例:
```("0" : "零") # 将 "0" 转写成 "零"
("" : " ") # 在指定的地方插入一个空格
("kg" : "kilogram") # 将 "kg" 或 "Kg" 扩展成 "kilogram" 
```
###2. 正则表达式RegexEntity
```
Form1: (/Matched expression/)
Form2: (/Matched expression/ : /Rewritten expression/)
```

样例:
```
(/\s+/ : / /) \#将一串连续的空格与换行符合并为一个空格
(/(\d+)\s?(-|~)\s?(\d+)/ : /$1 to $3/) #将 "15~20 dollars" 改写成 "15 to 20 dollars"
```

将用Matched匹配到字符串替换成Rewritten所表示的字符串。这里的正则表达式符合Perl正则规范。Form1只能作为匹配规则而不能作为转写规则，如果Rewritten为空，则只匹配不转写。Rewritten并不是真正的正则表达式，它仅支持普通字符串与`$1, $2, ..., $99，$n` 表示Matched expression匹配到的第n个Entity。 

###3. 脚本表达式 ScriptEntity
可以在文法中嵌入脚本，具体的语法规则由引擎所决定，目前可以嵌入Python。（详情可参考高级语法） 

-------
其他各类表达式，都是由这三类表达式进行组合得到的。它们的并（或操作），连接和差操作，构成了以下三类复合实体。这三种操作与正则表达式的三类基本操作一致。
表达式需要被其他表达式引用时，就需要为其命名，例如：
`entity= (/\s+/ : / /) ;`
这样就表达了一个名称为entity的字符串表达式。名称与c语言的变量命名规则一致。中间由=连接。最后由分号结束。

当引用其他表达式时，可以用$(RuleName)表达。


--------------------------------------------------------------------------------

###4. 或表达式 TableEntity
`Form: Table_name =Entity1 | Entity2 | …`
样例:
```
digit_0_to_9 = ("0" : "nol") | ("1" : "satu") | ("2" : "dua") | ("3" : "tiga") | ("4" : "empat") | ("5" : "lima") | ("6" : "enam") | ("7" : "tujuh") | ("8" : "delapan") | ("9" : "sembilan"); #印尼语数字 0~9 的Map 表
integer_int_extend = $(integer_int) | ("百" : "100") | ("千" : "1000") | ("万" : "10000") | ("亿" : "100000000");
```

integer_int_extend规则就是由integer_int和其他四个StringEntity构成的。
或表达式中间的分隔符有两种，竖线|和斜杠/。 以竖线分割的实体是平级的，会对每一个子表达式进行匹配，找出离字符串起始位置最近且匹配到的字符串最长的那个子表达式。而以斜杠分割的实体，被看做一组(Group)，一旦匹配，就不会匹配之后的表达式。可以在表达式中指定多个组合平级实体。
看下面的例子：
`grouptest= (/CD/) | (/ABC/) / (/AB/) | (/ABCD/);`
该规则分成了两组，在匹配ABCD时，前一组已经匹配了ABC,因此就不会继续向后匹配到ABCD。因此该规则最终匹配的结果是ABC. 

###5. 序列表达式 SequenceEntity
序列表达式描述了表达式的连接。序列从左到右依次匹配，一旦出现不能匹配的情况，则整个序列匹配失败。注意，序列匹配的字符串必须是相邻的。

```
integer_0_to_99 = $(integer_0_to_9) | $(integer_teens)
| $(integer_decades) $(del_0)
| $(integer_decades) $(ins_space) $(integer_1_to_9) $(ins_space);
```

这个表达式实际上是一个TableEntity，后两个子表达式是SequenceEntity。该表达式可以转写0~99范围内的整数。

匹配211时它首先用第一个integer_0_to_9能匹配到 '2'，再用第二个integer_teens能匹配到 "11"，再用第三个表达式匹配失败，再用第四个Sequence能匹配到 "21"，最终选择离起点最近且匹配到的字符串最长的那一个进行转写：
`211 ：twenty one`
序列表达式可以完成转写和顺序调整。例如：
`fraction = $(integer_int_extend) $(fraction_cnv_slash) $(integer_int) : $3 $2 $1 `

三分之一转写为1/3，integer_int_extend可以匹配‘三’, fraction_cnv_slash可匹配 '分之' , integer_int可匹配'一'。 $3 $2 $1 对其顺序进行了重排。

###6.重复表达式RepeatEntity
```
Form1: Repetition_name = $(an_entity)+;
Form2: Repetition_name = $(an_entity){m,n};
```
由一条需要重复的规则、要重复的次数以及结尾的分号组成。需要重复的规则有且仅有一条。所以不能写成
`error_example= $(an_entity0) $(an_entity){m,n}; `

m到n次，m是≥0的整数，n是≥0的整数或-1，为-1时表示不限制重复次数。 

这与正则表达式的规则基本一致。 

 
###7.差集表达式DiffEntity
```
Form1: Difference_name = $(Universe) - $(complement);
Form2: Difference_name = $(Universe) - $(complement1) - $(complement2) - …; 
```
由一组Complement以及结尾的分号组成。有且仅有一个Universe，后面用减号可以跟多个表达式。
当Universe表达式能匹配且其他complement不能匹配时成立。例如：
```
integer_1_to_9 = $(integer_0_to_9) - ("0" : "nol"); # 整数1~9
integer_2_to_999 = $(integer_0_to_999) - $(digit_1) - $(digit_0); # 整数2~999 
```

--------------------------------------------------------------------------------

###8. 元标签
可以为表达式增加标签，控制表达式的属性和功能。也可以引入规则等。 

####文件级元标签：
文件级元标签，不需要贴在任何规则之上。
`#%Include% Rules/cnext`
增加一个名称为cnext的外置文件。本文件中的规则即可引用该文件中的规则。支持双向引用。 

`#%Script% extends`
增加一个名称为extends.py的外置Python脚本。该标签适合在嵌入Python代码时使用。嵌入的代码可以执行外置脚本中定义的函数。引擎会在内部执行import(extends)函数。因此extends.py需要放置在规则文件同一级目录中。

####规则级元标签:
规则级元标签需要放在规则文本行之上，如：
```
#%Type% INT
#%Order% 180
int_0_4= $(int_0) | $(int_1) | $(int_2) | ("三" : "3") | ("四" : "4") ;
```
上面的两个标签意思分别为：
将int_0_4的类型标记为INT
将int_0_4的匹配优先级定义为140. 数字越大，优先级越低。 

不是所有的规则都是有效规则，有些规则只是被其他规则引用。只有加上#%Order%标签的才是有效规则。规则可以手动编写优先级。也可以省略之后的数字，引擎会自动根据引用结构来制定优先级，被引用层级越高的优先级越高。 

`#%Parameter% `为规则赋值
这部分取决于引擎的设计，将在《高级话题》中描述。 

####属性级元标签
在信息抽取时，属性元标签非常重要，它指定了引擎如何将文本转换为字典。

**案例1**：
```
#%Property% Denominator,,Numerator| Numerator ,, Denominator | Denominator ,, Numerator
fraction = $(integer_int_extend) $(fraction_cnv_slash) $(integer_int) : $3 $2 $1 |

$(integer_int) $(fraction2) $(integer_int) |

$(pure_decimal) ("" : "/") $(percent_transform);
```
属性标签为fraction的每一个引用实体增加了属性。 按照 '|' 分组，Denominator赋给integer_int_extend, Numerator赋给integer_int. 分别代表分子和分母。

**案例2**：

当抽取类似JSON或XML的文本时，抽取的字典需要以键值对的形式标注，如下例子： 
```
#%Property% ,$key,,$value
properties =$(space) $(name) $(equal) $(property) $(space);
```
则在抽取时，会以name为键，property为value, 插入抽取的字典中。 


--------------------------------------------------------------------------------

##9.注意事项

###注释
除了符合元标签格式的文本，以 # 开始的一行内容被认为是注释行被忽略。暂不支持在一行内容的中间或后面加注释，也不支持在某一规则的多行内容的中间插入一行注释。 

###换行
当Rule内容特别长时可以直接换行，中间插入的换行符/空格/制表符会被忽略，但不支持在中间插入注释行。 

###结束符
所有Rules都要以分号结束。 

###交叉引用
规则可以支持交叉引用，甚至可以引用自身，但被引用的表达式需要存在，否则会引发错误。引用时，需要保证文法不是左递归的，否则将会陷入死循环。 

###编码
由于文本处理引擎经常处理多国语言，因而要求使用UTF-8编码(no BOM)。