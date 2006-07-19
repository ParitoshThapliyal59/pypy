
// we hand craft these in module/support.ll
char *RPyString_AsString(RPyString*);
long RPyString_Size(RPyString*);
RPyString *RPyString_FromString(char *);
int _RPyExceptionOccurred(void);
char* LLVM_RPython_StartupCode(void);

#define RPyRaiseSimpleException(exctype, errormsg) raise##exctype(errormsg)

// XXX generated by rpython - argggh have to feed in prototypes
RPyFREXP_RESULT *ll_frexp_result(double, int);
RPyMODF_RESULT *ll_modf_result(double, double);
RPySTAT_RESULT *ll_stat_result(int, int, int, int, int, int, int, int, int, int);
void RPYTHON_RAISE_OSERROR(int error);
#ifdef RPyListOfString
  RPyListOfString *_RPyListOfString_New(long);
  void _RPyListOfString_SetItem(RPyListOfString *, int, RPyString *);
#endif

// XXX end of proto hacks
