using Cpp2IL.Core;
using AssetRipper.Primitives;
using System.Reflection;
using Iced.Intel;
using LibCpp2IL;
using System.Text.Json;
var tools=Path.GetFullPath("work/tools/Cpp2IL_net472");
System.Runtime.Loader.AssemblyLoadContext.Default.Resolving+=(ctx,n)=>{var p=Path.Combine(tools,n.Name+".dll");return File.Exists(p)?ctx.LoadFromAssemblyPath(p):null;};
new Cpp2IlCorePlugin().OnLoad();
var root=@"D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo";
Cpp2IlApi.InitializeLibCpp2Il(Path.Combine(root,"GameAssembly.dll"),Path.GetFullPath("outputs/STARHOME_Localization_0.2.0/backup_original/StarHome_Data/il2cpp_data/Metadata/global-metadata.dat"),UnityVersion.Parse("6000.3.15f1"));
var rows=new List<object>();var asmrows=new Dictionary<string,List<string>>();int count=0;
bool globals=args.Contains("globals");
var selected=new HashSet<uint>{5465,10207,6036,10664,10891,10211,10213,2449,3440,4827,13365,275,4451,2498,2640,2687,2691,2900,2954,3331,3420,4099,4127,4249,4440,4581,6302,6754,6985,7005,8037,8411,8579,8616,8727,9182,9422,9664,9959,10092,10254,11074,13379,13799,14184,14243,14235};
var app=Cpp2IlApi.CurrentAppContext!;
var methods=app.AllTypes.SelectMany(t=>t.Methods).Where(m=>m.UnderlyingPointer!=0).GroupBy(m=>m.UnderlyingPointer).ToDictionary(g=>g.Key,g=>string.Join(" | ",g.Take(3).Select(m=>m.FullName)));
foreach(var t in app.AllTypes.Where(t=>globals||t.FullName.StartsWith("Gameplay.")||t.FullName.StartsWith("Actions.")||t.FullName.StartsWith("Events.")||t.FullName.StartsWith("_Scripts.UI.")))
 foreach(var m in t.Methods.Where(m=>m.UnderlyingPointer!=0)) {
  var bytes=m.RawBytes.ToArray();if(bytes.Length==0)continue;count++;
  var decoder=Decoder.Create(64,new ByteArrayCodeReader(bytes));decoder.IP=m.UnderlyingPointer;var formatter=new IntelFormatter();var so=new StringOutput();var lines=new List<string>();bool any=false;
  while(decoder.IP<m.UnderlyingPointer+(ulong)bytes.Length) {
   decoder.Decode(out var ins);so.Reset();formatter.Format(ins,so);var note="";
   if(ins.IsIPRelativeMemoryOperand) {
    try { var u=LibCpp2IlMain.GetLiteralGlobalByAddress(ins.IPRelativeMemoryAddress);
     if(u!=null&&u.IsValid&&(!globals||selected.Contains(u.RawValue))) {var text=u.AsLiteral();note=" ; LITERAL "+u.RawValue+" "+JsonSerializer.Serialize(text);rows.Add(new{method=m.FullNameWithSignature,address=$"0x{m.UnderlyingPointer:X}",instruction=$"{ins.IP:X16} {so}",literal_index=u.RawValue,text});any=true;}
    }catch{}
   }
   if(ins.FlowControl is FlowControl.Call or FlowControl.UnconditionalBranch && ins.NearBranchTarget!=0&&methods.TryGetValue(ins.NearBranchTarget,out var name))note+=" ; "+name;
   lines.Add($"{ins.IP:X16} {so}"+note);
  }
  if(any)asmrows[m.FullNameWithSignature]=lines;
 }
File.WriteAllText("work/expanded_021/"+(globals?"global_final":"game")+"_literal_references.json",JsonSerializer.Serialize(rows,new JsonSerializerOptions{WriteIndented=true}));
File.WriteAllText("work/expanded_021/"+(globals?"global_final":"game")+"_literal_methods.json",JsonSerializer.Serialize(asmrows,new JsonSerializerOptions{WriteIndented=true}));
Console.WriteLine($"Methods {count}, literal references {rows.Count}");



