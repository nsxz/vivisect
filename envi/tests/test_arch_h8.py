
import envi
import envi.memory as e_mem
import envi.memcanvas as e_memcanvas
import envi.memcanvas.renderers as e_rend
import envi.archs.h8 as e_h8
import vivisect
import platform
import unittest
from envi import IF_RET, IF_NOFALL, IF_BRANCH, IF_CALL, IF_COND
from envi.archs.h8.const import *

instrs = [
        ( "8342", 0x4560, 'add.b #42, r3h', IF_B),
        ( "7c6075f0", 0x4560, 'bixor #7, @er6', 0),
        ( "7d507170", 0x4560, 'bnot #7, @er5', 0),
        ( "0832", 0x4560, 'add.b r3h, r2h', IF_B),
        ( "791d4745", 0x4560, 'add.w #4745, e5', IF_W),
        ( "0932", 0x4560, 'add.w r3, r2', IF_W),
        ( "7a1d00047145", 0x4560, 'add.l #47145, er5', IF_L),
        ( "01406930", 0x4560, 'ldc @er3, ccr', 0),
        ( "014069b0", 0x4560, 'stc ccr, @er3', 0),
        ( "01c05023", 0x4560, 'mulxs.b r2h, r3', IF_B),
        ( "01c05223", 0x4560, 'mulxs.w r2, er3', IF_W),
        ( "01d05123", 0x4560, 'divxs.b r2h, r3', IF_B),
        ( "01d05323", 0x4560, 'divxs.w r2, er3', IF_W),
        ( "01f06423", 0x4560, 'or.l er2, er3', IF_L),
        ( "01f06523", 0x4560, 'xor.l er2, er3', IF_L),
        ( "01f06623", 0x4560, 'and.l er2, er3', IF_L),
        ( "0a03", 0x4560, 'inc.b r3h', IF_B),
        ( "0a83", 0x4560, 'add.l er0, er3', IF_L),
        ( "0b83", 0x4560, 'adds #2, er3', 0),
        ( "0b93", 0x4560, 'adds #4, er3', 0),
        ( "0b53", 0x4560, 'inc.w #1, r3', IF_W),
        ( "0bf3", 0x4560, 'inc.l #2, er3', IF_L),
        ( "0f00", 0x4560, 'daa r0h', 0),
        ( "0f93", 0x4560, 'mov.l er1, er3', IF_L),
        ( "1a03", 0x4560, 'dec.b r3h', IF_B),
        ( "1a83", 0x4560, 'sub.l er0, er3', IF_L),
        ( "1b83", 0x4560, 'subs #2, er3', 0),
        ( "1b93", 0x4560, 'subs #4, er3', 0),
        ( "1b53", 0x4560, 'dec.w #1, r3', IF_W),
        ( "1bf3", 0x4560, 'dec.l #2, er3', IF_L),
        ( "1f00", 0x4560, 'das r0h', 0),
        ( "5470", 0x4560, 'rts', IF_RET | IF_NOFALL),
        ( "4670", 0x4560, 'bne #45d2', IF_BRANCH | IF_COND),
        ( "4e90", 0x4560, 'bgt #44f2', IF_BRANCH | IF_COND),
        ( "58500070", 0x4560, 'blo #45d4', IF_BRANCH | IF_COND),
        ( "58b0f070", 0x4560, 'bmi #35d4', IF_BRANCH | IF_COND),
        ( "01006df2", 0x4560, 'push.l er2', IF_L),
        ( "6dfa", 0x4560, 'push.w e2', IF_W),
        ( "6df2", 0x4560, 'push.w r2', IF_W),
        ( "6cda", 0x4560, 'mov.b r2l, @-er5', IF_B),
        ( '01006df2', 0x4560, 'push.l er2', IF_L),
        ( '6df2', 0x4560, 'push.w r2', IF_W),
        ( '6de2', 0x4560, 'mov.w r2, @-er6', IF_W),
        ( '6dda', 0x4560, 'mov.w e2, @-er5', IF_W),
        ( '01006dd2', 0x4560, 'mov.l er2, @-er5', IF_L),

        ]

class H8InstrTest(unittest.TestCase):
    def test_envi_h8_assorted_instrs(self):
       global instrs

       archmod = envi.getArchModule("h8")

       for bytez, va, reprOp, iflags in instrs:
            op = archmod.archParseOpcode(bytez.decode('hex'), 0, va)
            if repr(op).replace(' ','') != reprOp.replace(' ',''):
                raise Exception("FAILED to decode instr:  %.8x %s - should be: %s  - is: %s" % \
                        ( va, bytez, reprOp, repr(op) ) )
            self.assertEqual(op.iflags, iflags)

    #FIXME: test emuluation as well.


def generateTestInfo(ophexbytez='6e'):
    h8 = e_h8.H8Module()
    opbytez = ophexbytez
    op = h8.archParseOpcode(opbytez.decode('hex'), 0, 0x4000)
    print "opbytez = '%s'\noprepr = '%s'"%(opbytez,repr(op))
    opvars=vars(op)
    opers = opvars.pop('opers')
    print "opcheck = ",repr(opvars)

    opersvars = []
    for x in range(len(opers)):
        opervars = vars(opers[x])
        opervars.pop('_dis_regctx')
        opersvars.append(opervars)

    print "opercheck = %s" % (repr(opersvars))



raw_instrs = [
    ('8340'.decode('hex'), ),
    ('0832'.decode('hex'), ),
    ('79134715'.decode('hex'), ),
    ('0943'.decode('hex'), ),
    ('7a1300047145'.decode('hex'), ),
    ('0aa3'.decode('hex'), ),
    ('0b03'.decode('hex'), ),
    ('0b83'.decode('hex'), ),
    ('0b93'.decode('hex'), ),
    ('9340'.decode('hex'), ),
    ('0e43'.decode('hex'), ),
    ('e340'.decode('hex'), ),
    ('1643'.decode('hex'), ),
    ('79634715'.decode('hex'), ),
    ('6643'.decode('hex'), ),
    ('7a6300047145'.decode('hex'), ),
    ('01f06643'.decode('hex'), ),
    ('0640'.decode('hex'), ),
    ('01410640'.decode('hex'), ),
    ('7643'.decode('hex'), ),
    ('7c307640'.decode('hex'), ),
    ('7e477640'.decode('hex'), ),
    ('6a1047157640'.decode('hex'), ),
    ('6a30000471457640'.decode('hex'), ),
    ('4040'.decode('hex'), ),
    ('58004715'.decode('hex'), ),
    ('4150'.decode('hex'), ),
    ('58104715'.decode('hex'), ),
    ('4240'.decode('hex'), ),
    ('58204715'.decode('hex'), ),
    ('4340'.decode('hex'), ),
    ('58304715'.decode('hex'), ),
    ('4440'.decode('hex'), ),
    ('58404715'.decode('hex'), ),
    ('4540'.decode('hex'), ),
    ('58504715'.decode('hex'), ),
    ('4640'.decode('hex'), ),
    ('58604715'.decode('hex'), ),
    ('4740'.decode('hex'), ),
    ('58704715'.decode('hex'), ),
    ('4840'.decode('hex'), ),
    ('58804715'.decode('hex'), ),
    ('4940'.decode('hex'), ),
    ('58904715'.decode('hex'), ),
    ('4a40'.decode('hex'), ),
    ('58a04715'.decode('hex'), ),
    ('4b40'.decode('hex'), ),
    ('58b04715'.decode('hex'), ),
    ('4c40'.decode('hex'), ),
    ('58c04715'.decode('hex'), ),
    ('4d40'.decode('hex'), ),
    ('58d04715'.decode('hex'), ),
    ('4e40'.decode('hex'), ),
    ('58e04715'.decode('hex'), ),
    ('4f40'.decode('hex'), ),
    ('58f04715'.decode('hex'), ),
    ('7243'.decode('hex'), ),
    ('7d307240'.decode('hex'), ),
    ('7f407240'.decode('hex'), ),
    ('6a1847157240'.decode('hex'), ),
    ('6a38000471457240'.decode('hex'), ),
    ('6243'.decode('hex'), ),
    ('7d306240'.decode('hex'), ),
    ('7f406240'.decode('hex'), ),
    ('6a1847156240'.decode('hex'), ),
    ('6a38000471456240'.decode('hex'), ),
    ('76c3'.decode('hex'), ),
    ('7c3076c0'.decode('hex'), ),
    ('7e4076c0'.decode('hex'), ),
    ('6a10471576c0'.decode('hex'), ),
    ('6a300004714576c0'.decode('hex'), ),
    ('77c3'.decode('hex'), ),
    ('7c3077c0'.decode('hex'), ),
    ('7e4077c0'.decode('hex'), ),
    ('6a10471577c0'.decode('hex'), ),
    ('6a300004714577c0'.decode('hex'), ),
    ('74c3'.decode('hex'), ),
    ('7c3074c0'.decode('hex'), ),
    ('7e4074c0'.decode('hex'), ),
    ('6a10471574c0'.decode('hex'), ),
    ('6a300004714574c0'.decode('hex'), ),
    ('7d3067c0'.decode('hex'), ),
    ('7f4067c0'.decode('hex'), ),
    ('6a18471567c0'.decode('hex'), ),
    ('6a380004714567c0'.decode('hex'), ),
    ('75c3'.decode('hex'), ),
    ('7c3075c0'.decode('hex'), ),
    ('7e4075c0'.decode('hex'), ),
    ('6a10471575c0'.decode('hex'), ),
    ('6a300004714575c0'.decode('hex'), ),
    ('7743'.decode('hex'), ),
    ('7c307740'.decode('hex'), ),
    ('7e407740'.decode('hex'), ),
    ('6a1047157740'.decode('hex'), ),
    ('6a30000471457740'.decode('hex'), ),
    ('7143'.decode('hex'), ),
    ('7d307140'.decode('hex'), ),
    ('7f407140'.decode('hex'), ),
    ('6a1847157140'.decode('hex'), ),
    ('6a38000471457140'.decode('hex'), ),
    ('6143'.decode('hex'), ),
    ('7d306140'.decode('hex'), ),
    ('7f406140'.decode('hex'), ),
    ('6a1847156140'.decode('hex'), ),
    ('6a38000471456140'.decode('hex'), ),
    ('7443'.decode('hex'), ),
    ('7c307440'.decode('hex'), ),
    ('7e407440'.decode('hex'), ),
    ('6a1047157440'.decode('hex'), ),
    ('6a30000471457440'.decode('hex'), ),
    ('7043'.decode('hex'), ),
    ('7d307040'.decode('hex'), ),
    ('7f407040'.decode('hex'), ),
    ('6a1847157040'.decode('hex'), ),
    ('6a38000471457040'.decode('hex'), ),
    ('6043'.decode('hex'), ),
    ('7d306040'.decode('hex'), ),
    ('7f406040'.decode('hex'), ),
    ('6a1847156040'.decode('hex'), ),
    ('6a38000471456040'.decode('hex'), ),
    ('5542'.decode('hex'), ),
    ('5c004242'.decode('hex'), ),
    ('6743'.decode('hex'), ),
    ('7d306740'.decode('hex'), ),
    ('7f406740'.decode('hex'), ),
    ('6a1847156740'.decode('hex'), ),
    ('6a38000471456740'.decode('hex'), ),
    ('7343'.decode('hex'), ),
    ('7c307340'.decode('hex'), ),
    ('7e407340'.decode('hex'), ),
    ('6a1047157340'.decode('hex'), ),
    ('6a30000471457340'.decode('hex'), ),
    ('6343'.decode('hex'), ),
    ('7c306340'.decode('hex'), ),
    ('7e406340'.decode('hex'), ),
    ('6a1047156340'.decode('hex'), ),
    ('6a30000471456340'.decode('hex'), ),
    ('7543'.decode('hex'), ),
    ('7c307540'.decode('hex'), ),
    ('7e407540'.decode('hex'), ),
    ('6a1047157540'.decode('hex'), ),
    ('6a30000471457540'.decode('hex'), ),
    ('a340'.decode('hex'), ),
    ('1c43'.decode('hex'), ),
    ('79234715'.decode('hex'), ),
    ('1d43'.decode('hex'), ),
    ('7a2300047145'.decode('hex'), ),
    ('1fc3'.decode('hex'), ),
    ('0f03'.decode('hex'), ),
    ('1f03'.decode('hex'), ),
    ('1a03'.decode('hex'), ),
    ('1b53'.decode('hex'), ),
    ('1bd3'.decode('hex'), ),
    ('1b73'.decode('hex'), ),
    ('1bf3'.decode('hex'), ),
    ('01d05143'.decode('hex'), ),
    ('01d05343'.decode('hex'), ),
    ('5143'.decode('hex'), ),
    ('5343'.decode('hex'), ),
    ('7b5c598f'.decode('hex'), ),
    ('7bd4598f'.decode('hex'), ),
    ('17d3'.decode('hex'), ),
    ('17f3'.decode('hex'), ),
    ('1753'.decode('hex'), ),
    ('1773'.decode('hex'), ),
    ('0a03'.decode('hex'), ),
    ('0b53'.decode('hex'), ),
    ('0bd3'.decode('hex'), ),
    ('0b73'.decode('hex'), ),
    ('0bf3'.decode('hex'), ),
    ('5940'.decode('hex'), ),
    ('5a047145'.decode('hex'), ),
    ('5b41'.decode('hex'), ),
    ('5d40'.decode('hex'), ),
    ('5e047145'.decode('hex'), ),
    ('5f41'.decode('hex'), ),
    ('0740'.decode('hex'), ),
    ('01410740'.decode('hex'), ),
    ('0304'.decode('hex'), ),
    ('0314'.decode('hex'), ),
    ('01406940'.decode('hex'), ),
    ('01416940'.decode('hex'), ),
    ('01406f404715'.decode('hex'), ),
    ('01416f404715'.decode('hex'), ),
    ('014078406b2000047145'.decode('hex'), ),
    ('014178406b2000047145'.decode('hex'), ),
    ('01406d40'.decode('hex'), ),
    ('01416d40'.decode('hex'), ),
    ('01406b004715'.decode('hex'), ),
    ('01416b004715'.decode('hex'), ),
    ('01406b2000047145'.decode('hex'), ),
    ('01416b2000047145'.decode('hex'), ),
    ('01106d74'.decode('hex'), ),
    ('01206d74'.decode('hex'), ),
    ('01306d74'.decode('hex'), ),
    ('f340'.decode('hex'), ),
    ('0c43'.decode('hex'), ),
    ('6843'.decode('hex'), ),
    ('6e434715'.decode('hex'), ),
    ('78406a2300047145'.decode('hex'), ),
    ('6c43'.decode('hex'), ),
    ('2340'.decode('hex'), ),
    ('6a034715'.decode('hex'), ),
    ('78306a2300047145'.decode('hex'), ),
    ('6cb4'.decode('hex'), ),
    ('3440'.decode('hex'), ),
    ('6a844715'.decode('hex'), ),
    ('6aa400047145'.decode('hex'), ),
    ('79044715'.decode('hex'), ),
    ('0d43'.decode('hex'), ),
    ('6943'.decode('hex'), ),
    ('6f434715'.decode('hex'), ),
    ('78406b2300047145'.decode('hex'), ),
    ('6d43'.decode('hex'), ),
    ('6b034715'.decode('hex'), ),
    ('6b2300047145'.decode('hex'), ),
    ('69b4'.decode('hex'), ),
    ('6fb44715'.decode('hex'), ),
    ('78306ba400047145'.decode('hex'), ),
    ('6db4'.decode('hex'), ),
    ('6b844715'.decode('hex'), ),
    ('6ba400047145'.decode('hex'), ),
    ('7a0300047145'.decode('hex'), ),
    ('0fc3'.decode('hex'), ),
    ('01006943'.decode('hex'), ),
    ('01006f434715'.decode('hex'), ),
    ('010078406b2300047145'.decode('hex'), ),
    ('01006d43'.decode('hex'), ),
    ('01006b034715'.decode('hex'), ),
    ('01006b2300047145'.decode('hex'), ),
    ('010069b4'.decode('hex'), ),
    ('01006fb44715'.decode('hex'), ),
    ('010078306ba400047145'.decode('hex'), ),
    ('01006db4'.decode('hex'), ),
    ('01006b844715'.decode('hex'), ),
    ('01006ba400047145'.decode('hex'), ),
    ('01c05043'.decode('hex'), ),
    ('01c05243'.decode('hex'), ),
    ('5043'.decode('hex'), ),
    ('5243'.decode('hex'), ),
    ('1783'.decode('hex'), ),
    ('1793'.decode('hex'), ),
    ('17b3'.decode('hex'), ),
    ('0000'.decode('hex'), ),
    ('1703'.decode('hex'), ),
    ('1713'.decode('hex'), ),
    ('1733'.decode('hex'), ),
    ('c340'.decode('hex'), ),
    ('1443'.decode('hex'), ),
    ('79434715'.decode('hex'), ),
    ('6443'.decode('hex'), ),
    ('7a4300047145'.decode('hex'), ),
    ('01f06443'.decode('hex'), ),
    ('0440'.decode('hex'), ),
    ('01410440'.decode('hex'), ),
    ('6d74'.decode('hex'), ),
    ('01006d74'.decode('hex'), ),
    ('6df4'.decode('hex'), ),
    ('01006df4'.decode('hex'), ),
    ('1283'.decode('hex'), ),
    ('12c3'.decode('hex'), ),
    ('1293'.decode('hex'), ),
    ('12d3'.decode('hex'), ),
    ('12b3'.decode('hex'), ),
    ('12f3'.decode('hex'), ),
    ('1383'.decode('hex'), ),
    ('13c3'.decode('hex'), ),
    ('1393'.decode('hex'), ),
    ('13d3'.decode('hex'), ),
    ('13b3'.decode('hex'), ),
    ('13f3'.decode('hex'), ),
    ('1203'.decode('hex'), ),
    ('1243'.decode('hex'), ),
    ('1213'.decode('hex'), ),
    ('1253'.decode('hex'), ),
    ('1233'.decode('hex'), ),
    ('1273'.decode('hex'), ),
    ('1303'.decode('hex'), ),
    ('1343'.decode('hex'), ),
    ('1313'.decode('hex'), ),
    ('1353'.decode('hex'), ),
    ('1333'.decode('hex'), ),
    ('1373'.decode('hex'), ),
    ('5670'.decode('hex'), ),
    ('5470'.decode('hex'), ),
    ('1083'.decode('hex'), ),
    ('10c3'.decode('hex'), ),
    ('1093'.decode('hex'), ),
    ('10d3'.decode('hex'), ),
    ('10b3'.decode('hex'), ),
    ('10f3'.decode('hex'), ),
    ('1183'.decode('hex'), ),
    ('11c3'.decode('hex'), ),
    ('1193'.decode('hex'), ),
    ('11d3'.decode('hex'), ),
    ('11b3'.decode('hex'), ),
    ('11f3'.decode('hex'), ),
    ('1003'.decode('hex'), ),
    ('1043'.decode('hex'), ),
    ('1013'.decode('hex'), ),
    ('1053'.decode('hex'), ),
    ('1033'.decode('hex'), ),
    ('1073'.decode('hex'), ),
    ('1103'.decode('hex'), ),
    ('1143'.decode('hex'), ),
    ('1113'.decode('hex'), ),
    ('1153'.decode('hex'), ),
    ('1133'.decode('hex'), ),
    ('1173'.decode('hex'), ),
    ('0180'.decode('hex'), ),
    ('0203'.decode('hex'), ),
    ('0213'.decode('hex'), ),
    ('014069b0'.decode('hex'), ),
    ('014169b0'.decode('hex'), ),
    ('01406fb04715'.decode('hex'), ),
    ('01416fb04715'.decode('hex'), ),
    ('014078306ba000047145'.decode('hex'), ),
    ('014178306ba000047145'.decode('hex'), ),
    ('01406d30'.decode('hex'), ),
    ('01416d30'.decode('hex'), ),
    ('01406b804715'.decode('hex'), ),
    ('01416b804715'.decode('hex'), ),
    ('01406ba000047145'.decode('hex'), ),
    ('01416ba000047145'.decode('hex'), ),
    ('01106df3'.decode('hex'), ),
    ('01206df3'.decode('hex'), ),
    ('01306df3'.decode('hex'), ),
    ('1843'.decode('hex'), ),
    ('79334715'.decode('hex'), ),
    ('1943'.decode('hex'), ),
    ('7a3300047145'.decode('hex'), ),
    ('1ac3'.decode('hex'), ),
    ('1b03'.decode('hex'), ),
    ('1b83'.decode('hex'), ),
    ('1b93'.decode('hex'), ),
    ('b340'.decode('hex'), ),
    ('1e43'.decode('hex'), ),
    ('01e07b3c'.decode('hex'), ),
    ('5730'.decode('hex'), ),
    ('d340'.decode('hex'), ),
    ('1543'.decode('hex'), ),
    ('79434715'.decode('hex'), ),
    ('6543'.decode('hex'), ),
    ('7a5300047145'.decode('hex'), ),
    ('01f06543'.decode('hex'), ),
    ('0540'.decode('hex'), ),
    ('01410540'.decode('hex'), ),
    ]

if __name__ == '__main__':
    h8m = envi.getArchModule('h8')      

    for instr in raw_instrs:
        inst = instr[0]
        op = h8m.archParseOpcode(inst, 0, 0x50)
        print "%26s %s" % (instr[0].encode('hex'), op)
        if len(op) != len(inst):
            #raise Exception(" LENGTH FAILURE:  expected: %d  real: %d  '%s'" % (len(inst), len(op), inst.encode('hex')))
            print(" LENGTH FAILURE:  expected: %d  real: %d  '%s'" % (len(inst), len(op), inst.encode('hex')))

