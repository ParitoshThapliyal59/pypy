from pypy.rpython.annlowlevel import llhelper
from pypy.jit.metainterp.history import JitCellToken
from pypy.jit.backend.test.calling_convention_test import TestCallingConv, parse
from pypy.rpython.lltypesystem import lltype
from pypy.jit.codewriter.effectinfo import EffectInfo
from pypy.jit.backend.arm.test.support import skip_unless_arm
skip_unless_arm()


class TestARMCallingConvention(TestCallingConv):
    # ../../test/calling_convention_test.py

    def test_call_argument_spilling(self):
        # bug when we have a value in r0, that is overwritten by an argument
        # and needed after the call, so that the register gets spilled after it
        # was overwritten with the argument to the call
        def func(a):
            return a + 16

        I = lltype.Signed
        FUNC = self.FuncType([I], I)
        FPTR = self.Ptr(FUNC)
        func_ptr = llhelper(FPTR, func)
        calldescr = self.cpu.calldescrof(FUNC, FUNC.ARGS, FUNC.RESULT, EffectInfo.MOST_GENERAL)
        funcbox = self.get_funcbox(self.cpu, func_ptr)

        args = ', '.join(['i%d' % i for i in range(11)])
        ops = """
        [%s]
        i99 = call(ConstClass(func_ptr), 22, descr=calldescr)
        finish(%s, i99)""" % (args, args)
        loop = parse(ops, namespace=locals())
        looptoken = JitCellToken()
        self.cpu.compile_loop(loop.inputargs, loop.operations, looptoken)
        args = [x for x in range(11)]
        self.cpu.execute_token(looptoken, *args)
        for x in range(11):
            assert self.cpu.get_latest_value_int(x) == x
        assert self.cpu.get_latest_value_int(11) == 38