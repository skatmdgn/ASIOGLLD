// @category ASIOGLLD
// Read-only Ghidra headless export. The original executable is not modified.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;
import java.io.BufferedWriter;
import java.util.HashMap;
import java.util.Map;

public class ExportAsioRecovery extends GhidraScript {
    private final Map<Long,String> known = new HashMap<>();
    private void prepare() {
        long[] a = {0x1050,0x1060,0x1070,0x16B0,0x1650,0x1690,0x16A0,0x1740,0x1770,
            0x1910,0x1930,0x1C50,0x1AD0,0x1AA0,0x1960,0x1BD0,0x1C00,0x17E0,0x1C10,0x1C90,
            0x1D40,0x1DC0,0x5FA0};
        String[] n = {"QI","AddRef","Release","Init","GetDriverName","GetDriverVersion",
            "GetErrorMessage","Start","Stop","GetChannels","GetLatencies","GetBufferSize",
            "CanSampleRate","GetSampleRate","SetSampleRate","GetClockSources","SetClockSource",
            "GetSamplePosition","GetChannelInfo","CreateBuffers","DisposeBuffers","ControlPanel","UnsupportedStub"};
        for(int i=0;i<a.length;i++)known.put(a[i],"CAsio_"+n[i]);
        known.put(0x67E0,"MMDeviceEnumerator_Create");
        known.put(0x3870,"AudioPort_WASAPI_InitCandidate");
        known.put(0x92B0,"AudioWorker_SetupCandidate");
        known.put(0x97B0,"PortEventDispatcherCandidate");
        known.put(0x8FC0,"AudioWorker_StartCandidate");
        known.put(0x94B0,"AudioWorker_TeardownCandidate");
    }
    @Override public void run() throws Exception {
        prepare();
        String[] args=getScriptArgs();
        if(args.length==0)throw new IllegalArgumentException("Expected output directory");
        Path root=Paths.get(args[0]).toAbsolutePath();
        Path funcs=root.resolve("functions");
        Files.createDirectories(funcs);
        DecompInterface decomp=new DecompInterface();
        decomp.setSimplificationStyle("decompile");
        if(!decomp.openProgram(currentProgram))throw new IllegalStateException("Decompiler open failed");
        long base=currentProgram.getImageBase().getOffset();
        int pass=0,fail=0,total=0;
        try(BufferedWriter index=Files.newBufferedWriter(root.resolve("functions.tsv"),StandardCharsets.UTF_8)){
            index.write("rva\tname\tsize_bytes\tstatus\trecovered_label\n");
            FunctionIterator it=currentProgram.getFunctionManager().getFunctions(true);
            while(it.hasNext()){
                monitor.checkCancelled();
                Function f=it.next();
                long rva=f.getEntryPoint().getOffset()-base;
                String id=String.format("%08X",rva);
                String label=known.getOrDefault(rva,"");
                String status="failed";
                try{
                    DecompileResults result=decomp.decompileFunction(f,45,monitor);
                    if(result.decompileCompleted() && result.getDecompiledFunction()!=null){
                        String src="/* Original RVA 0x"+id+"; pseudocode only; suggested label: "+label+" */\n"+result.getDecompiledFunction().getC();
                        Files.writeString(funcs.resolve(id+".c"),src,StandardCharsets.UTF_8);
                        status="ok";pass++;
                    }else fail++;
                }catch(Exception ignored){fail++;}
                index.write(String.format("0x%X\t%s\t%d\t%s\t%s\n",rva,f.getName(),f.getBody().getNumAddresses(),status,label));
                total++;
            }
        }finally{decomp.dispose();}
        String summary="Ghidra functions: "+total+"\nDecompiled: "+pass+"\nFailed: "+fail+"\nOriginal unmodified.\n";
        Files.writeString(root.resolve("SUMMARY.txt"),summary,StandardCharsets.UTF_8);
        println(summary);
    }
}
