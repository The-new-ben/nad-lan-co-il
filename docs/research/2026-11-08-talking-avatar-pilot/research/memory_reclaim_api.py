"""Import-safe Windows memory query/reclaim helpers; no process opened on import."""
import ctypes
from ctypes import wintypes
import time
kernel=ctypes.WinDLL('kernel32',use_last_error=True);psapi=ctypes.WinDLL('psapi',use_last_error=True)
kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];kernel.OpenProcess.restype=wintypes.HANDLE
kernel.CloseHandle.argtypes=[wintypes.HANDLE]
kernel.QueryFullProcessImageNameW.argtypes=[wintypes.HANDLE,wintypes.DWORD,wintypes.LPWSTR,ctypes.POINTER(wintypes.DWORD)]
kernel.GetProcessTimes.argtypes=[wintypes.HANDLE]+[ctypes.POINTER(wintypes.FILETIME)]*4
kernel.GetExitCodeProcess.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)]
psapi.EmptyWorkingSet.argtypes=[wintypes.HANDLE];psapi.EmptyWorkingSet.restype=wintypes.BOOL
class Memory(ctypes.Structure):
    _fields_=[('length',wintypes.DWORD),('load',wintypes.DWORD)]+[(name,ctypes.c_uint64) for name in ('total','available','pageTotal','pageAvailable','virtualTotal','virtualAvailable','extended')]
class Counters(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('faults',wintypes.DWORD)]+[(name,ctypes.c_size_t) for name in ('peakWorking','working','peakPaged','paged','peakNonpaged','nonpaged','pagefile','peakPagefile','private')]
psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD]
def times(handle):
    values=[wintypes.FILETIME() for _ in range(4)]
    if not kernel.GetProcessTimes(handle,*[ctypes.byref(value) for value in values]):raise ctypes.WinError(ctypes.get_last_error())
    seconds=[((value.dwHighDateTime<<32)|value.dwLowDateTime)/1e7 for value in values]
    return seconds[0]-11644473600,seconds[2]+seconds[3]
def memory():
    value=Memory();value.length=ctypes.sizeof(value)
    if not kernel.GlobalMemoryStatusEx(ctypes.byref(value)):raise ctypes.WinError(ctypes.get_last_error())
    return {'at':time.time(),'availableGiB':round(value.available/1024**3,4),'commitCapacityAvailableGiB':round(value.pageAvailable/1024**3,4)}
def counters(handle):
    value=Counters();value.cb=ctypes.sizeof(value)
    if not psapi.GetProcessMemoryInfo(handle,ctypes.byref(value),value.cb):raise ctypes.WinError(ctypes.get_last_error())
    exitcode=wintypes.DWORD();kernel.GetExitCodeProcess(handle,ctypes.byref(exitcode))
    return {'workingMiB':round(value.working/1024**2,3),'privateCommittedMiB':round(value.private/1024**2,3),'pageFaultCount':value.faults,'alive':exitcode.value==259}
class Pressure:
    def __init__(self):
        self.api=ctypes.WinDLL('pdh');self.query=wintypes.HANDLE();self.handles={};self.error=None
        self.api.PdhOpenQueryW.argtypes=[wintypes.LPCWSTR,ctypes.c_size_t,ctypes.POINTER(wintypes.HANDLE)]
        self.api.PdhAddEnglishCounterW.argtypes=[wintypes.HANDLE,wintypes.LPCWSTR,ctypes.c_size_t,ctypes.POINTER(wintypes.HANDLE)]
        self.api.PdhCollectQueryData.argtypes=[wintypes.HANDLE]
        self.api.PdhCloseQuery.argtypes=[wintypes.HANDLE]
        result=self.api.PdhOpenQueryW(None,0,ctypes.byref(self.query))
        if result:self.error=int(result);return
        for key,path in [('pagesInputPerSecond',r'\Memory\Pages Input/sec'),('pageReadsPerSecond',r'\Memory\Page Reads/sec'),('pagesOutputPerSecond',r'\Memory\Pages Output/sec')]:
            handle=wintypes.HANDLE();result=self.api.PdhAddEnglishCounterW(self.query,path,0,ctypes.byref(handle))
            if result:self.error=int(result)
            else:self.handles[key]=handle
        self.api.PdhCollectQueryData(self.query)
    def sample(self):
        if self.error:return {'counterReadError':self.error}
        class Value(ctypes.Structure):_fields_=[('status',wintypes.DWORD),('value',ctypes.c_double)]
        self.api.PdhGetFormattedCounterValue.argtypes=[wintypes.HANDLE,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD),ctypes.POINTER(Value)]
        self.api.PdhCollectQueryData(self.query);out={}
        for key,handle in self.handles.items():
            value=Value();result=self.api.PdhGetFormattedCounterValue(handle,0x200,None,ctypes.byref(value))
            out[key]=round(value.value,3) if result==0 and value.status in (0,1) else None
        return out
    def close(self):
        if self.query:self.api.PdhCloseQuery(self.query)
