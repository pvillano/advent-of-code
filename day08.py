
from math import *
from itertools import *
from collections import *

img = '222222222222222122222222222222122122022022222222120202222202202220202222202022022022222222022202222222102122222212220222122022022222222202222222212222222222222222222022222222222222122022222222222222100212222202222221202222212122022022022222022202222222022022222202221222122222022222222202222222222222222222222222222122222222222222022022022122222222012202222222202220202222222022122222222220122222222222122022222212222222122222022222222212222222202222222222222222222122222222222222022222122122222222020202222222222222222222202222222122022221222202222222212122222212221222222122022222222202222222222222222222222222222022222222222222222222022122222022212212222222222220222222222122122122022221222222222222102022222212222222022022222221222222222222222222222222222222222222222222222222022122222022222122202212222222212221222222202122122222122220022222222222202222222212221222022022222220222202222222202222222222222222222222222222222222222122122022222022000222222222202221222222212122122122022220222202222222002222222222220222122222022221222222222222222222222222222222222122222222222222022022022222222022111212222202202220202220222022022022222221222212222222112022222212222222222022022222222222222222212222222222222222222022222222222222222022222122022222011212222212212220201221212222222022222222222222222222202122222202220222222222022222222222222222212222222222222222220222222222222222122222122022122022122202222222222221222220222222122122122221222212222222222022222202220222222222022222222202222222012222222222222222220122222222222222122222222222022122202212222212212222212220222122022222222222122222222222002122222202222222222022222221222222222222012222222222222222220022222222222222022222122122022022101202222222212221210221212122122022222220222222222222202022222222220222122022222222222212222222012222222222222222222122222222222222022122222122122222222222222212212222210222212222122022022222222212222222012122222222222222222222022222222222222222002222222222222022220222222222222222222222022122122022222212222222222220212221222122122122122221222212222222222222222212220222022122122220222222222222102222222222222022220022222222222222022222022222122122200222222202222220222221202222122222022222022202222222202022222210222222122222022220222222222222212222222222222122221122222222222222022022122222022222200222222222222220222220212222122222222221122222220022202022222200220222022022022220222212222222002222222222222222220222222222222222022122122122222022110212222212212220220220202122222122122221222212221122022222222210221222022022222222222202222222222222222222222222220022222222222222122222122222222022101222222202202222201220212122022122122220222202220222112022222202221222122122222221222202222222122222222222222122222222222222222222022122122222222222222202222202202220202221202222222222022222222212220222012222222202220222222122222222222202222222212222222222222122221122222222222222022222022022222122121202222202212222221220212222122022022221122012222122202222222220221222222222222222222202222222112222222222222222220022222222222222222122022122122222021222222212202220211222202122122122222221022102122022102022222211221222022122222221222222222222102222222222222022220222222222222222122222222222222222210202222212222221201221212022222022222222222022222222122222222210220222022122020220222212222222112222222222222222222022222222222222222022122122122122110222222212222222221220212222122222022220221202020222122222222220220222022022020220222222222222202222222222222222222222222222222222222122122122122022112212222212202221201221212022222222122222022222122222102122222212222222122122222221222222222222112222222222222222222022222222222222222122022222022222101212222202222222211221212022122022022222020002121222202022222201221222122022220220222212222222222222222212222122222122222222222222122022122222222022200212222202202221211221222022022022122220120102022122022222222212222222222022122222222222222222222222222212222122222222222222222222022022222022222122212222222222202221211221212022222022222220221202121022022222222211220222122222020222222202222222012222222212222122222122222222222222220122222122022222000202222222222222220221212122022022222222220212120022202122222201220222222122020222222202222222102222222222222022221022222222222222122122222122022122210222222212202221202222212222122122222222122212022122002022222200222222022122222222222222222222202222222202222222221022222222222222220122022022122022100212222222222221200220202122022022122221020012021022012022222220220222222122122221222122222222112222222212222222221122222222022222221122022222022022211212222222212220201220212222122222222222020202122022022022222222220222222222222221222112222222222222202202222122221222222222112222020222222022022022201202222202212222221222222222022022122221021212122222212222222220221222022122221220222022222222002222222212222122221222222222022222020122022220222022222202222212212222201222212022122022222221221122020222112222222202220222222122022222222222222222222222212202222022220222222222202222022122122222122022102212222212222222212220212222222022222222221112120022212022222001220222222122121221222102222222202222222202222122220222222222102222020222122120222222202222222212222222211222212022022222022220122222220222212022222110221222122222221221222202222220122222212212222222221022222222122222120022222221122022210202222202222222222220212022022122022221021022121222112122222000220222122122222220222102222221002222222222222222220222222222112222022222022021222222212202222212222222202221202022022122022222120102121022012222222002221222022022020220222012222221112222202212222222221022222222012222120222222022222122202202222212212222221221212222022222122222022022022122212222222101222222222222020221222222222220022222222202222022220222222222100222222022122020102022002212222212212222201222212022222022222220222112020022002122222102222222222122122222222222222221212222212202222222222122222222222222221122122022101022112212222202212222200221202122122122122221021012121222002122222122220222222222120220222112222211102222202222222022220122222222100222122022222122000022200222222222212221200222222022122022022220221102022222102220222222220222222102122221222212222211222212212212222022220222222222211222022222122221020222111212222212212220221221222222222121122220121222120022022220222100222222222222022222222202222201012222212202222122220122222222221222121222022121022222201222222202202221201221202222122020022222021112022222002220222002220222122222122221222112222210112222202202222222221122222222211222120122222122210022002212222212202222220222202022122221222221120122221222002022222211220222222102122222222102222220212202212220222222220022222222220222021122021022102222122222222222202220221222202221122020022222222012022122112220222001222222022112120221222112222200202202222220222022220222222222202222120122021021121122220212222202222222212222212120022122022222221012021022112221222010220222122002220220222112222221002202202220222022220122212222220221020222221220020022211212222212202222202221222220122220022222120202020022012021222011222222022122022222222102222220222222222221222022222122202222100222221222121020110222010222222200212221220222222002022021222220020112220222012222222020222222222212022220222102222220102222202200222222222022222221022221222122022220201022001202222212212221212220202011222121022220120012220122212021222021020222222102022222222222222202212212212211222022221022202222101222222122020121010122211212222220212220221222202121022021122222121012022122222221222110220222122212122221222222222201122202222202222122220122222220101222121222021021111022001222222212212220211222212210022221022221120022122222212021222220221222022112122220222022222212002222220201222022220222202222210220122122021221221222122212222201202222211220222222222222122220222122222222122122222200221222022002022222222012222202212222221212222022221022222221020221120222021121101222110202222212202221211222202112222222122221001202222122122220222111120222022122220221222112222200022212210211222122221222202221200220021122221021122122020222222210202222212222202102022120022221112002121122022022222001122222022212220222222022222220202202211210222122220122212212001220121122221222010022121212222202212221210221212212122121222220112022021122212121222111120222022202220221222212222211112122221220222222222222212210021222121122020020210122101212212221212220221222202011022122122220111022022022202222222121222222222122221222212012222202122212220210222212221022222200000222020222122121201222201222202221212221222220222010222220222221212112122022002020222022120222122222022222212022222211202222222220122202221122222221102221122122021121221022120212222221222222201222202120222122022220200012220122022221222201022222022202122222202102222221222212210201122102222222212211200222122122222021002122101202202201212222220222202220222222022220001122121022012122222202022222122122222221212222222220122112220211122022222122202202101221220122122221122022122202212220202220201222212010022222122222212012121122222021222001020222222102022220202112222211012202202222122212222022212210001220121122121221002222210222222202202121210221222012102220022222020002022122012221222210220222222222222220212012222202002222210210122212220022202221222222121222222121200022010212202212202120200220212010112021222220000212220022222220222122122222122122020222222212222202122202220200022002222222212221220220120122222121101222110222212201202022210202202221012022222220020222020122202122222001221222222002220222222012222201212202211200022012220222221222201221121022120121110022222202222222202122200222212001022022022222110002120222102022222111121222122022121221222022220200202102221201122122222222202201110222221022122220102122222202202220212220201211202100212021222220011222222022102222222120020222122102121220122122220220022222201200022002221022212212012220121122120220120222221212222210212120222211212121022120022220102122222022002121222022122222222022220222122112222202202102222201012212222122201202212222220022122121121022011212202222202022212002202100002220122222020122221022102020222211121222022222122221012022222200012002221201022022222122222221121222221222120122021222210202202201222020202220202022012120022220011002020222102022222222222222022222120221012202220220022122212220112002220022201221010220122222222121110022201222212202202221211101222021221221222221011122121122012121222220020222022022220220202022220212212112200200202012220222212202120220022022122121111122221222202211212202210201222021112222222220210002021222202121222201021222222222222221002012221221202212200010202222222022212202010220120122221220021222001212222201202022211201222202022021122222111212220222202021222000020222022122121221112222220210102022212200102202221122210212211221001222222122011022120212222200202102200100222021021021222221002022221222202222222122021222222112021220012222222220022212201211212022220122210222110220022222121221001222012212222222222212211211222210000020222221010120022022002221222012121222022002211221212022220212012212222201112022220122221222012220201222021220011222020202202221222012200122212222012020122220100012120222122220202101022220122022000220202222221212012222222111012122222122201221101220220122022022210122201212212201202121211111222200121121222222000002120022102022112102221220222102210221202122222210122022210111112212221122221221112220012022120020010122120202202200212021201100212102220020222221000011122122222121022221120221022002122221022002222220122022210100102211222122201210200222110222122020202122110222212222200100210111202210211121212221122020022122120221212100022221222012222222222002221212002002200201112102220222200212011221022022121120200022022222222202220201222001202220200020122222011210201222120122122022022222222022022221112112221210102202201012212112222122211220202221122022222221202222012222222201201011210112212010200122022222211011101022011022022210022220122222221222222202221221202112211222222120220122212222211221102222021022122022201222212210201212201111222012021221112221210210202122110222102202220222022012020222022002220211002112202202112121221122200201100222002022222220110122021212222212212210211200202221212020102221202220121222210022212110000220222202101221212212221210002112211001012122222022220222202222122102221020011022012212222212201221202020202222101221122221001200112222222000222010212222022022200220122002220200022022212210222011122122202202110222122212122212212122221202222212210122212222222221210220112221001201112222212111222202112221122122102220212112220210002122220201102202122022200210100220212212021020221022022202202200222121210112222102000122012221100210012222222100202002110222122002020221202002221220012022222200102012020122211210120222220122121202100022221212222220212110211212202001000222002222101102211222000200111002020221122122001222202202222212222222222200122000221122212202201221202221222111100222000212212201220121222220202012222120112220201002012022022000010122211221122122222222002102220210211012212012102220222222220212100220010012222011110122112212212221202000220221202012002221222222201220222022120022012201110221002212122222112012221212010122200200002111220122201221022221122212221100100022111212212220202222200200202212121121122221101221010022201001001102120222102002020022222102220211202202221211122002022120201200120222120021020211211222100202212022222210201012222121101221212221210210122022111112200122210220002002212220020102222221220122221200112211001122202212220220011120022020011022222222212220201202221011202020020010102222211102121022111221010112012222102022100221002202222210021212200001102220022122220211002220112120220011222122111202222221212212211111202210100101212222212120120222102112010000002221022102022120022022221221002102221212212211201121210210021220110110120211111022222202020101201212210110202110000212102222211211012022210102222010220221102002201222000212221212002112220111012211201120221200100220121200020102201022101202001212202021211211222010001221212221011201121022202200221202022221212102221220022122220211222222200210122022121022212212111222220120022210200122120112102120210222200020212211022101202222110211101222022220112211000220212122010221211202222201200212200020012201021122220101201221021010121212212122111122001000220220211021212220011100022220201201002122221212100212220221112012020121101212220211122222220020012001100120022211221221222221020001222022202022122021221001220221222222201020002220212010001122202200101010022220212112210221122012221221010102222022122111101022200102200222120001022212022122110122101011212211200100112002222120022221001122000222010111122222111220102002012122011212220212120222221202222021001120011010221221010201020102001022112122000220220010212111012210120022022222001020202122101111001200211221202002110022010002221211111012211211202111221121110000122222100211020000021222002001121202220220211221012002121210002222101221201222010020200121110220022202202221001202220210111222122202010021122000202110212001210202001111110100002110101022112211120202020202112012221101110111110100221010122221202100220100221201012100101010100120'

width = 25
height = 6
area = width*height

for r in range(height):
    print()
    for c in range(width):
        for i in range(len(img)//area):
            px = img[i*area:(i+1)*area][c+r*width]
            if px != '2':
                print(' █'[int(px)], end='')
                break


