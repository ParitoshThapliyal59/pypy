import autopath
from pypy.objspace.std import stringobject
from pypy.objspace.std.stringobject import W_StringObject


objspacename = 'std'

class TestW_StringObject:

    def teardown_method(self,method):
        pass

##    def test_order_rich(self):
##        space = self.space
##        def w(txt):
##             return W_StringObject(space, txt)
##        strs = ['ala', 'bla', 'ala', 'alaaa', '', 'b']
##        ops = [ 'EQ', 'LT', 'GT', 'NE', 'LE', 'GE' ]

##        while strs[1:]:
##            str1 = strs.pop()
##            for op in ops:
##                 #original python function
##                orf = getattr(str1, '__%s__' % op.lower()) 
##                pypyconst = getattr(stringobject, op)
##                for str2 in strs:   
##                    if orf(str2):
##                         self.failUnless_w(
##                             string_richcompare(space,
##                                                w(str1),
##                                                w(str2),
##                                                pypyconst))
##                    else:
##                         self.failIf_w(
##                             string_richcompare(space,
##                                                w(str1),
##                                                w(str2),
##                                                pypyconst))
        

    def test_str_w(self):
        assert self.space.str_w(self.space.wrap("foo")) == "foo"

    def test_equality(self):
        w = self.space.wrap 
        assert self.space.eq_w(w('abc'), w('abc'))
        assert not self.space.eq_w(w('abc'), w('def'))

    def test_order_cmp(self):
        space = self.space
        w = space.wrap
        assert self.space.is_true(space.lt(w('a'), w('b')))
        assert self.space.is_true(space.lt(w('a'), w('ab')))
        assert self.space.is_true(space.le(w('a'), w('a')))
        assert self.space.is_true(space.gt(w('a'), w('')))

    def test_truth(self):
        w = self.space.wrap
        assert self.space.is_true(w('non-empty'))
        assert not self.space.is_true(w(''))

    def test_getitem(self):
        space = self.space
        w = space.wrap
        w_str = w('abc')
        assert self.space.eq_w(space.getitem(w_str, w(0)), w('a'))
        assert self.space.eq_w(space.getitem(w_str, w(-1)), w('c'))
        self.space.raises_w(space.w_IndexError,
                            space.getitem,
                            w_str,
                            w(3))

    def test_slice(self):
        space = self.space
        w = space.wrap
        w_str = w('abc')

        w_slice = space.newslice(w(0), w(0), None)
        assert self.space.eq_w(space.getitem(w_str, w_slice), w(''))

        w_slice = space.newslice(w(0), w(1), None)
        assert self.space.eq_w(space.getitem(w_str, w_slice), w('a'))

        w_slice = space.newslice(w(0), w(10), None)
        assert self.space.eq_w(space.getitem(w_str, w_slice), w('abc'))

        w_slice = space.newslice(space.w_None, space.w_None, None)
        assert self.space.eq_w(space.getitem(w_str, w_slice), w('abc'))

        w_slice = space.newslice(space.w_None, w(-1), None)
        assert self.space.eq_w(space.getitem(w_str, w_slice), w('ab'))

        w_slice = space.newslice(w(-1), space.w_None, None)
        assert self.space.eq_w(space.getitem(w_str, w_slice), w('c'))

    def test_extended_slice(self):
        space = self.space
        if self.space.__class__.__name__.startswith('Trivial'):
            import sys
            if sys.version < (2, 3):
                return
        w_None = space.w_None
        w = space.wrap
        w_str = w('hello')

        w_slice = space.newslice(w_None, w_None, w(1))
        assert self.space.eq_w(space.getitem(w_str, w_slice), w('hello'))

        w_slice = space.newslice(w_None, w_None, w(-1))
        assert self.space.eq_w(space.getitem(w_str, w_slice), w('olleh'))

        w_slice = space.newslice(w_None, w_None, w(2))
        assert self.space.eq_w(space.getitem(w_str, w_slice), w('hlo'))

        w_slice = space.newslice(w(1), w_None, w(2))
        assert self.space.eq_w(space.getitem(w_str, w_slice), w('el'))

class AppTestStringObject:
    def test_format_wrongchar(self):
        raises(ValueError, 'a%Zb'.__mod__, ((23,),))

    def test_split(self):
        assert "".split() == []
        assert "a".split() == ['a']
        assert " a ".split() == ['a']
        assert "a b c".split() == ['a','b','c']
        assert 'this is the split function'.split() == ['this', 'is', 'the', 'split', 'function']
        assert 'a|b|c|d'.split('|') == ['a', 'b', 'c', 'd']
        assert 'a|b|c|d'.split('|', 2) == ['a', 'b', 'c|d']
        assert 'a b c d'.split(None, 1) == ['a', 'b c d']
        assert 'a b c d'.split(None, 2) == ['a', 'b', 'c d']
        assert 'a b c d'.split(None, 3) == ['a', 'b', 'c', 'd']
        assert 'a b c d'.split(None, 4) == ['a', 'b', 'c', 'd']
        assert 'a b c d'.split(None, 0) == ['a b c d']
        assert 'a  b  c  d'.split(None, 2) == ['a', 'b', 'c  d']
        assert 'a b c d '.split() == ['a', 'b', 'c', 'd']
        assert 'a//b//c//d'.split('//') == ['a', 'b', 'c', 'd']
        assert 'endcase test'.split('test') == ['endcase ', '']

    def test_split_splitchar(self):
        assert "/a/b/c".split('/') == ['','a','b','c']

    def test_title(self):
        assert "brown fox".title() == "Brown Fox"
        assert "!brown fox".title() == "!Brown Fox"
        assert "bROWN fOX".title() == "Brown Fox"
        assert "Brown Fox".title() == "Brown Fox"
        assert "bro!wn fox".title() == "Bro!Wn Fox"

    def test_istitle(self):
        assert "brown fox".istitle() == False
        assert "!brown fox".istitle() == False
        assert "bROWN fOX".istitle() == False
        assert "Brown Fox".istitle() == True
        assert "bro!wn fox".istitle() == False
        assert "Bro!wn fox".istitle() == False
        assert "!brown Fox".istitle() == False
        assert "!Brown Fox".istitle() == True
        assert "Brow&&&&N Fox".istitle() == True
        assert "!Brow&&&&n Fox".istitle() == False
        
    def test_capitalize(self):
        assert "brown fox".capitalize() == "Brown fox"
        assert ' hello '.capitalize() == ' hello '
        assert 'Hello '.capitalize() == 'Hello '
        assert 'hello '.capitalize() == 'Hello '
        assert 'aaaa'.capitalize() == 'Aaaa'
        assert 'AaAa'.capitalize() == 'Aaaa'

    def test_rjust(self):
        s = "abc"
        assert s.rjust(2) == s
        assert s.rjust(3) == s
        assert s.rjust(4) == " " + s
        assert s.rjust(5) == "  " + s
        assert 'abc'.rjust(10) == '       abc'
        assert 'abc'.rjust(6) == '   abc'
        assert 'abc'.rjust(3) == 'abc'
        assert 'abc'.rjust(2) == 'abc'

    def test_ljust(self):
        s = "abc"
        assert s.ljust(2) == s
        assert s.ljust(3) == s
        assert s.ljust(4) == s + " "
        assert s.ljust(5) == s + "  "
        assert 'abc'.ljust(10) == 'abc       '
        assert 'abc'.ljust(6) == 'abc   '
        assert 'abc'.ljust(3) == 'abc'
        assert 'abc'.ljust(2) == 'abc'

    def test_replace(self):
        assert 'one!two!three!'.replace('!', '@', 1) == 'one@two!three!'
        assert 'one!two!three!'.replace('!', '') == 'onetwothree'
        assert 'one!two!three!'.replace('!', '@', 2) == 'one@two@three!'
        assert 'one!two!three!'.replace('!', '@', 3) == 'one@two@three@'
        assert 'one!two!three!'.replace('!', '@', 4) == 'one@two@three@'
        assert 'one!two!three!'.replace('!', '@', 0) == 'one!two!three!'
        assert 'one!two!three!'.replace('!', '@') == 'one@two@three@'
        assert 'one!two!three!'.replace('x', '@') == 'one!two!three!'
        assert 'one!two!three!'.replace('x', '@', 2) == 'one!two!three!'
        assert 'abc'.replace('', '-') == '-a-b-c-'
        assert 'abc'.replace('', '-', 3) == '-a-b-c'
        assert 'abc'.replace('', '-', 0) == 'abc'
        assert ''.replace('', '') == ''
        assert 'abc'.replace('ab', '--', 0) == 'abc'
        assert 'abc'.replace('xy', '--') == 'abc'
        assert '123'.replace('123', '') == ''
        assert '123123'.replace('123', '') == ''
        assert '123x123'.replace('123', '') == 'x'


    def test_strip(self):
        s = " a b "
        assert s.strip() == "a b"
        assert s.rstrip() == " a b"
        assert s.lstrip() == "a b "
        assert 'xyzzyhelloxyzzy'.strip('xyz') == 'hello'
        assert 'xyzzyhelloxyzzy'.lstrip('xyz') == 'helloxyzzy'
        assert 'xyzzyhelloxyzzy'.rstrip('xyz') == 'xyzzyhello'

    def test_zfill(self):
        assert '123'.zfill(2) == '123'
        assert '123'.zfill(3) == '123'
        assert '123'.zfill(4) == '0123'
        assert '+123'.zfill(3) == '+123'
        assert '+123'.zfill(4) == '+123'
        assert '+123'.zfill(5) == '+0123'
        assert '-123'.zfill(3) == '-123'
        assert '-123'.zfill(4) == '-123'
        assert '-123'.zfill(5) == '-0123'
        assert ''.zfill(3) == '000'
        assert '34'.zfill(1) == '34'
        assert '34'.zfill(4) == '0034'
            
    def test_center(self):
        s="a b"
        assert s.center(0) == "a b"
        assert s.center(1) == "a b"
        assert s.center(2) == "a b"
        assert s.center(3) == "a b"
        assert s.center(4) == "a b "
        assert s.center(5) == " a b "
        assert s.center(6) == " a b  "
        assert s.center(7) == "  a b  "
        assert s.center(8) == "  a b   "
        assert s.center(9) == "   a b   "
        assert 'abc'.center(10) == '   abc    '
        assert 'abc'.center(6) == ' abc  '
        assert 'abc'.center(3) == 'abc'
        assert 'abc'.center(2) == 'abc'

        
    def test_count(self):
        assert "".count("x") ==0
        assert "".count("") ==1
        assert "Python".count("") ==7
        assert "ab aaba".count("ab") ==2
        assert 'aaa'.count('a') == 3
        assert 'aaa'.count('b') == 0
        assert 'aaa'.count('a', -1) == 1
        assert 'aaa'.count('a', -10) == 3
        assert 'aaa'.count('a', 0, -1) == 2
        assert 'aaa'.count('a', 0, -10) == 0
    
    
    def test_startswith(self):
        assert 'ab'.startswith('ab') == 1
        assert 'ab'.startswith('a') == 1
        assert 'ab'.startswith('') == 1
        assert 'x'.startswith('a') == 0
        assert 'x'.startswith('x') == 1
        assert ''.startswith('') == 1
        assert ''.startswith('a') == 0
        assert 'x'.startswith('xx') == 0
        assert 'y'.startswith('xx') == 0
                

    def test_endswith(self):
        assert 'ab'.endswith('ab') == 1
        assert 'ab'.endswith('b') == 1
        assert 'ab'.endswith('') == 1
        assert 'x'.endswith('a') == 0
        assert 'x'.endswith('x') == 1
        assert ''.endswith('') == 1
        assert ''.endswith('a') == 0
        assert 'x'.endswith('xx') == 0
        assert 'y'.endswith('xx') == 0
      
    def test_expandtabs(self):
        assert 'abc\rab\tdef\ng\thi'.expandtabs() ==    'abc\rab      def\ng       hi'
        assert 'abc\rab\tdef\ng\thi'.expandtabs(8) ==   'abc\rab      def\ng       hi'
        assert 'abc\rab\tdef\ng\thi'.expandtabs(4) ==   'abc\rab  def\ng   hi'
        assert 'abc\r\nab\tdef\ng\thi'.expandtabs(4) == 'abc\r\nab  def\ng   hi'
        assert 'abc\rab\tdef\ng\thi'.expandtabs() ==    'abc\rab      def\ng       hi'
        assert 'abc\rab\tdef\ng\thi'.expandtabs(8) ==   'abc\rab      def\ng       hi'
        assert 'abc\r\nab\r\ndef\ng\r\nhi'.expandtabs(4) == 'abc\r\nab\r\ndef\ng\r\nhi'

        s = 'xy\t'
        assert s.expandtabs() =='xy      '
        
        s = '\txy\t'
        assert s.expandtabs() =='        xy      '
        assert s.expandtabs(1) ==' xy '
        assert s.expandtabs(2) =='  xy  '
        assert s.expandtabs(3) =='   xy '
        
        assert 'xy'.expandtabs() =='xy'
        assert ''.expandtabs() ==''


    def test_splitlines(self):
        s="ab\nab\n \n  x\n\n\n"
        assert s.splitlines() ==['ab',    'ab',  ' ',   '  x',   '',    '']
        assert s.splitlines() ==s.splitlines(0)
        assert s.splitlines(1) ==['ab\n', 'ab\n', ' \n', '  x\n', '\n', '\n']
        s="\none\n\two\nthree\n\n"
        assert s.splitlines() ==['', 'one', '\two', 'three', '']
        assert s.splitlines(1) ==['\n', 'one\n', '\two\n', 'three\n', '\n']
    
    def test_find(self):
        assert 'abcdefghiabc'.find('abc') == 0
        assert 'abcdefghiabc'.find('abc', 1) == 9
        assert 'abcdefghiabc'.find('def', 4) == -1

    def test_index(self):
        assert 'abcdefghiabc'.index('') == 0
        assert 'abcdefghiabc'.index('def') == 3
        assert 'abcdefghiabc'.index('abc') == 0
        assert 'abcdefghiabc'.index('abc', 1) == 9
        #XXX it comes UnicodeError
        #self.assertRaises(ValueError, 'abcdefghiabc'.index('hib'))
        #self.assertRaises(ValueError, 'abcdefghiab'.index('abc', 1))
        #self.assertRaises(ValueError, 'abcdefghi'.index('ghi', 8))
        #self.assertRaises(ValueError, 'abcdefghi'.index('ghi', -1))

    def test_rfind(self):
        assert 'abcdefghiabc'.rfind('abc') == 9
        assert 'abcdefghiabc'.rfind('') == 12
        assert 'abcdefghiabc'.rfind('abcd') == 0
        assert 'abcdefghiabc'.rfind('abcz') == -1

    def test_rindex(self):
        assert 'abcdefghiabc'.rindex('') == 12
        assert 'abcdefghiabc'.rindex('def') == 3
        assert 'abcdefghiabc'.rindex('abc') == 9
        assert 'abcdefghiabc'.rindex('abc', 0, -1) == 0
        #XXX it comes UnicodeError
        #self.assertRaises(ValueError, 'abcdefghiabc'.rindex('hib'))
        #self.assertRaises(ValueError, 'defghiabc'.rindex('def', 1))
        #self.assertRaises(ValueError, 'defghiabc'.rindex('abc', 0, -1))
        #self.assertRaises(ValueError, 'abcdefghi'.rindex('ghi', 0, 8))
        #self.assertRaises(ValueError, 'abcdefghi'.rindex('ghi', 0, -1))


    def test_split_maxsplit(self):
        assert "/a/b/c".split('/', 2) == ['','a','b/c']
        assert "a/b/c".split("/") == ['a', 'b', 'c']
        assert " a ".split(None, 0) == ['a ']
        assert " a ".split(None, 1) == ['a']
        assert " a a ".split(" ", 0) == [' a a ']
        assert " a a ".split(" ", 1) == ['', 'a a ']

    def test_join(self):
        assert ", ".join(['a', 'b', 'c']) == "a, b, c"
        assert "".join([]) == ""
        assert "-".join(['a', 'b']) == 'a-b'
        raises(TypeError, ''.join, 1)
        raises(TypeError, ''.join, [1])
        raises(TypeError, ''.join, [[1]])

    def test_lower(self):
        assert "aaa AAA".lower() == "aaa aaa"
        assert "".lower() == ""

    def test_upper(self):
        assert "aaa AAA".upper() == "AAA AAA"
        assert "".upper() == ""

    def test_isalnum(self):
        assert "".isalnum() == False
        assert "!Bro12345w&&&&n Fox".isalnum() == False
        assert "125 Brown Foxes".isalnum() == False
        assert "125BrownFoxes".isalnum() == True

    def test_isalpha(self):
        assert "".isalpha() == False
        assert "!Bro12345w&&&&nFox".isalpha() == False
        assert "Brown Foxes".isalpha() == False
        assert "125".isalpha() == False

    def test_isdigit(self):
        assert "".isdigit() == False
        assert "!Bro12345w&&&&nFox".isdigit() == False
        assert "Brown Foxes".isdigit() == False
        assert "125".isdigit() == True

    def test_isspace(self):
        assert "".isspace() == False
        assert "!Bro12345w&&&&nFox".isspace() == False
        assert " ".isspace() ==  True
        assert "\t\t\b\b\n".isspace() == False
        assert "\t\t".isspace() == True
        assert "\t\t\r\r\n".isspace() == True
        
    def test_islower(self):
        assert "".islower() == False
        assert " ".islower() ==  False
        assert "\t\t\b\b\n".islower() == False
        assert "b".islower() == True
        assert "bbb".islower() == True
        assert "!bbb".islower() == False
        assert "BBB".islower() == False
        assert "bbbBBB".islower() == False

    def test_isupper(self):
        assert "".isupper() == False
        assert " ".isupper() ==  False
        assert "\t\t\b\b\n".isupper() == False
        assert "B".isupper() == True
        assert "BBB".isupper() == True
        assert "!BBB".isupper() == False
        assert "bbb".isupper() == False
        assert "BBBbbb".isupper() == False
                          
         
    def test_swapcase(self):
        assert "aaa AAA 111".swapcase() == "AAA aaa 111"
        assert "".swapcase() == ""

    def test_translate(self):
        def maketrans(origin, image):
            if len(origin) != len(image):
                raise ValueError("maketrans arguments must have same length")
            L = [chr(i) for i in range(256)]
            for i in range(len(origin)):
                L[ord(origin[i])] = image[i]

            tbl = ''.join(L)
            return tbl
        
        table = maketrans('abc', 'xyz')
        assert 'xyzxyz' == 'xyzabcdef'.translate(table, 'def')

        table = maketrans('a', 'A')
        assert 'Abc' == 'abc'.translate(table)
        assert 'xyz' == 'xyz'.translate(table)
        assert 'yz' ==  'xyz'.translate(table, 'x')
        
        #self.assertRaises(ValueError, 'xyz'.translate('too short', 'strip'))
        #self.assertRaises(ValueError, 'xyz'.translate('too short'))

    def test_iter(self):
        l=[]
        for i in iter("42"):
            l.append(i)
        assert l == ['4','2']
        
    def test_repr(self):
        assert repr("")       =="''"
        assert repr("a")      =="'a'"
        assert repr("'")      =='"\'"'
        assert repr("\'")     =="\"\'\""
        assert repr("\"")     =='\'"\''
        assert repr("\t")     =="'\\t'"
        assert repr("\\")     =="'\\\\'"
        assert repr('')       =="''"
        assert repr('a')      =="'a'"
        assert repr('"')      =="'\"'"
        assert repr('\'')     =='"\'"'
        assert repr('\"')     =="'\"'"
        assert repr('\t')     =="'\\t'"
        assert repr('\\')     =="'\\\\'"
        assert repr("'''\"")  =='\'\\\'\\\'\\\'"\''
        assert repr(chr(19))  =="'\\x13'"
        assert repr(chr(2))   =="'\\x02'"

    def test_contains(self):
        assert '' in 'abc'
        assert 'a' in 'abc'
        assert 'ab' in 'abc'
        assert not 'd' in 'abc'
        raises(TypeError, 'a'.__contains__, 1)
