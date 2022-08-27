/*
   This file has been generated by IDA.
   It contains local type definitions from
   the type library 'x86_vs.exe'
*/

#define __int8 char
#define __int16 short
#define __int32 int
#define __int64 long long

union _LARGE_INTEGER;
struct _EXCEPTION_RECORD;
struct _CONTEXT;
struct _s_ThrowInfo;
struct _s_CatchableTypeArray;
struct _s_CatchableType;
struct TypeDescriptor;
struct _RTL_CRITICAL_SECTION_DEBUG;

/* 1 */
enum __TI_flags
{
  TI_IsConst = 0x1,
  TI_IsVolatile = 0x2,
  TI_IsUnaligned = 0x4,
  TI_IsPure = 0x8,
  TI_IsWinRT = 0x10,
};

/* 2 */
enum __CT_flags
{
  CT_IsSimpleType = 0x1,
  CT_ByReferenceOnly = 0x2,
  CT_HasVirtualBase = 0x4,
  CT_IsWinRTHandle = 0x8,
  CT_IsStdBadAlloc = 0x10,
};

/* 3 */
typedef struct _SCOPETABLE_ENTRY *PSCOPETABLE_ENTRY;

/* 21 */
typedef void *PVOID;

/* 11 */
typedef unsigned int DWORD;

/* 4 */
struct _EH3_EXCEPTION_REGISTRATION
{
  struct _EH3_EXCEPTION_REGISTRATION *Next;
  PVOID ExceptionHandler;
  PSCOPETABLE_ENTRY ScopeTable;
  DWORD TryLevel;
};

/* 5 */
typedef struct _EH3_EXCEPTION_REGISTRATION EH3_EXCEPTION_REGISTRATION;

/* 6 */
typedef struct _EH3_EXCEPTION_REGISTRATION *PEH3_EXCEPTION_REGISTRATION;

/* 7 */
struct CPPEH_RECORD
{
  DWORD old_esp;
  EXCEPTION_POINTERS *exc_ptr;
  struct _EH3_EXCEPTION_REGISTRATION registration;
};

/* 8 */
struct _EH4_SCOPETABLE_RECORD
{
  int EnclosingLevel;
  void *FilterFunc;
  void *HandlerFunc;
};

/* 9 */
struct _EH4_SCOPETABLE
{
  DWORD GSCookieOffset;
  DWORD GSCookieXOROffset;
  DWORD EHCookieOffset;
  DWORD EHCookieXOROffset;
  struct _EH4_SCOPETABLE_RECORD ScopeRecord[];
};

/* 10 */
struct _FILETIME
{
  DWORD dwLowDateTime;
  DWORD dwHighDateTime;
};

/* 12 */
typedef _LARGE_INTEGER LARGE_INTEGER;

/* 15 */
typedef int LONG;

/* 14 */
struct _LARGE_INTEGER::$837407842DC9087486FDFA5FEB63B74E
{
  DWORD LowPart;
  LONG HighPart;
};

/* 16 */
typedef __int64 LONGLONG;

/* 13 */
union _LARGE_INTEGER
{
  struct
  {
    DWORD LowPart;
    LONG HighPart;
  };
  _LARGE_INTEGER::$837407842DC9087486FDFA5FEB63B74E u;
  LONGLONG QuadPart;
};

/* 19 */
typedef _EXCEPTION_RECORD EXCEPTION_RECORD;

/* 18 */
typedef EXCEPTION_RECORD *PEXCEPTION_RECORD;

/* 24 */
typedef _CONTEXT CONTEXT;

/* 23 */
typedef CONTEXT *PCONTEXT;

/* 17 */
struct _EXCEPTION_POINTERS
{
  PEXCEPTION_RECORD ExceptionRecord;
  PCONTEXT ContextRecord;
};

/* 22 */
typedef unsigned int ULONG_PTR;

/* 20 */
struct _EXCEPTION_RECORD
{
  DWORD ExceptionCode;
  DWORD ExceptionFlags;
  _EXCEPTION_RECORD *ExceptionRecord;
  PVOID ExceptionAddress;
  DWORD NumberParameters;
  ULONG_PTR ExceptionInformation[15];
};

/* 28 */
typedef unsigned __int8 BYTE;

/* 27 */
struct _FLOATING_SAVE_AREA
{
  DWORD ControlWord;
  DWORD StatusWord;
  DWORD TagWord;
  DWORD ErrorOffset;
  DWORD ErrorSelector;
  DWORD DataOffset;
  DWORD DataSelector;
  BYTE RegisterArea[80];
  DWORD Spare0;
};

/* 26 */
typedef _FLOATING_SAVE_AREA FLOATING_SAVE_AREA;

/* 25 */
#pragma pack(push, 4)
struct _CONTEXT
{
  DWORD ContextFlags;
  DWORD Dr0;
  DWORD Dr1;
  DWORD Dr2;
  DWORD Dr3;
  DWORD Dr6;
  DWORD Dr7;
  FLOATING_SAVE_AREA FloatSave;
  DWORD SegGs;
  DWORD SegFs;
  DWORD SegEs;
  DWORD SegDs;
  DWORD Edi;
  DWORD Esi;
  DWORD Ebx;
  DWORD Edx;
  DWORD Ecx;
  DWORD Eax;
  DWORD Ebp;
  DWORD Eip;
  DWORD SegCs;
  DWORD EFlags;
  DWORD Esp;
  DWORD SegSs;
  BYTE ExtendedRegisters[512];
};
#pragma pack(pop)

/* 30 */
typedef unsigned int UINT;

/* 29 */
struct _cpinfo
{
  UINT MaxCharSize;
  BYTE DefaultChar[2];
  BYTE LeadByte[12];
};

/* 32 */
typedef unsigned __int64 ULONGLONG;

/* 35 */
struct _SINGLE_LIST_ENTRY
{
  _SINGLE_LIST_ENTRY *Next;
};

/* 34 */
typedef _SINGLE_LIST_ENTRY SLIST_ENTRY;

/* 36 */
typedef unsigned __int16 WORD;

/* 33 */
struct _SLIST_HEADER::$04C3B4B3818F1694974352AE64BF5082
{
  SLIST_ENTRY Next;
  WORD Depth;
  WORD CpuId;
};

/* 31 */
union _SLIST_HEADER
{
  ULONGLONG Alignment;
  struct
  {
    SLIST_ENTRY Next;
    WORD Depth;
    WORD CpuId;
  };
};

/* 38 */
typedef const _s_ThrowInfo ThrowInfo;

/* 37 */
typedef ThrowInfo _ThrowInfo;

/* 40 */
typedef void (__cdecl *PMFN)(void *);

/* 41 */
typedef const _s_CatchableTypeArray CatchableTypeArray;

/* 39 */
#pragma pack(push, 4)
struct _s_ThrowInfo
{
  unsigned int attributes;
  PMFN pmfnUnwind;
  int (__cdecl *pForwardCompat)();
  CatchableTypeArray *pCatchableTypeArray;
};
#pragma pack(pop)

/* 43 */
typedef const _s_CatchableType CatchableType;

/* 42 */
#pragma pack(push, 4)
struct _s_CatchableTypeArray
{
  int nCatchableTypes;
  CatchableType *arrayOfCatchableTypes[];
};
#pragma pack(pop)

/* 46 */
#pragma pack(push, 4)
struct PMD
{
  int mdisp;
  int pdisp;
  int vdisp;
};
#pragma pack(pop)

/* 44 */
#pragma pack(push, 4)
struct _s_CatchableType
{
  unsigned int properties;
  TypeDescriptor *pType;
  PMD thisDisplacement;
  int sizeOrOffset;
  PMFN copyFunction;
};
#pragma pack(pop)

/* 45 */
struct TypeDescriptor
{
  void *pVFTable;
  void *spare;
  char name[];
};

/* 47 */
struct FuncInfo
{
  int magicNumber;
  int maxState;
  void *pUnwindMap;
  int nTryBlocks;
  void *pTryBlockMap;
  int nIPMapEntries;
  void *pIPtoStateMap;
  void *pESTypeList;
  int EHFlags;
};

/* 48 */
struct UnwindMapEntry
{
  int toState;
  void *action;
};

/* 49 */
struct TryBlockMapEntry
{
  int tryLow;
  int tryHigh;
  int catchHigh;
  int nCatches;
  void *pHandlerArray;
};

/* 50 */
struct HandlerType
{
  int adjectives;
  void *pType;
  int dispCatchObj;
  void *addressOfHandler;
};

/* 51 */
enum _crt_argv_mode
{
  _crt_argv_no_arguments = 0x0,
  _crt_argv_unexpanded_arguments = 0x1,
  _crt_argv_expanded_arguments = 0x2,
};

/* 53 */
typedef void (__cdecl *_PVFV)();

/* 52 */
#pragma pack(push, 8)
struct _onexit_table_t
{
  _PVFV *_first;
  _PVFV *_last;
  _PVFV *_end;
};
#pragma pack(pop)

/* 57 */
typedef unsigned __int16 wchar_t;

/* 56 */
typedef wchar_t WCHAR;

/* 55 */
typedef WCHAR *LPWSTR;

/* 58 */
typedef BYTE *LPBYTE;

/* 59 */
typedef void *HANDLE;

/* 54 */
struct _STARTUPINFOW
{
  DWORD cb;
  LPWSTR lpReserved;
  LPWSTR lpDesktop;
  LPWSTR lpTitle;
  DWORD dwX;
  DWORD dwY;
  DWORD dwXSize;
  DWORD dwYSize;
  DWORD dwXCountChars;
  DWORD dwYCountChars;
  DWORD dwFillAttribute;
  DWORD dwFlags;
  WORD wShowWindow;
  WORD cbReserved2;
  LPBYTE lpReserved2;
  HANDLE hStdInput;
  HANDLE hStdOutput;
  HANDLE hStdError;
};

/* 60 */
#pragma pack(push, 8)
struct fenv_t
{
  unsigned int _Fe_ctl;
  unsigned int _Fe_stat;
};
#pragma pack(pop)

/* 61 */
struct boost::exception_detail::clone_base;

/* 62 */
struct std::exception;

/* 64 */
typedef _RTL_CRITICAL_SECTION_DEBUG *PRTL_CRITICAL_SECTION_DEBUG;

/* 63 */
#pragma pack(push, 8)
struct _RTL_CRITICAL_SECTION
{
  PRTL_CRITICAL_SECTION_DEBUG DebugInfo;
  LONG LockCount;
  LONG RecursionCount;
  HANDLE OwningThread;
  HANDLE LockSemaphore;
  ULONG_PTR SpinCount;
};
#pragma pack(pop)

/* 67 */
struct _LIST_ENTRY
{
  _LIST_ENTRY *Flink;
  _LIST_ENTRY *Blink;
};

/* 66 */
typedef _LIST_ENTRY LIST_ENTRY;

/* 65 */
struct _RTL_CRITICAL_SECTION_DEBUG
{
  WORD Type;
  WORD CreatorBackTraceIndex;
  _RTL_CRITICAL_SECTION *CriticalSection;
  LIST_ENTRY ProcessLocksList;
  DWORD EntryCount;
  DWORD ContentionCount;
  DWORD Flags;
  WORD CreatorBackTraceIndexHigh;
  WORD SpareWORD;
};

/* 68 */
struct __crt_stdio_output::formatting_buffer;

/* 69 */
struct __crt_mbstring;

/* 71 */
typedef int __ehstate_t;

/* 70 */
#pragma pack(push, 4)
struct EHRegistrationNode
{
  EHRegistrationNode *pNext;
  void *frameHandler;
  __ehstate_t state;
};
#pragma pack(pop)

/* 72 */
#pragma pack(push, 8)
struct __crt_locale_pointers
{
  struct __crt_locale_data *locinfo;
  struct __crt_multibyte_data *mbcinfo;
};
#pragma pack(pop)

/* 73 */
struct _LocaleUpdate;

/* 74 */
enum _crt_exit_cleanup_mode
{
  _crt_exit_full_cleanup = 0x0,
  _crt_exit_quick_cleanup = 0x1,
  _crt_exit_no_cleanup = 0x2,
};

/* 75 */
enum _crt_exit_return_mode
{
  _crt_exit_terminate_process = 0x0,
  _crt_exit_return_to_caller = 0x1,
};

/* 76 */
struct CatchTableTypeArray
{
  int dwCount;
  int ppCatchTableType;
};

/* 77 */
struct CatchTableType
{
  int flag;
  int pTypeInfo;
  float thisDisplacement;
  int sizeOrOffset;
  int pCopyFunction;
};

