using System.Reflection.Metadata;
using System.Reflection.PortableExecutable;
using System.Text.Json;
using Cpp2IL.Core;
using AssetRipper.Primitives;
using Iced.Intel;

if(args.Contains("enumvalues")) {
 using var pe=new PEReader(File.OpenRead("work/prototype_evidence/dummy_dll/Assembly-CSharp.dll"));
 var md=pe.GetMetadataReader();
 foreach(var th in md.TypeDefinitions) { var t=md.GetTypeDefinition(th); if(md.GetString(t.Name)!="Resources") continue;
 foreach(var fh in t.GetFields()) {var f=md.GetFieldDefinition(fh);var ch=f.GetDefaultValue();if(!ch.IsNil){var c=md.GetConstant(ch);var br=md.GetBlobReader(c.Value);Console.WriteLine(md.GetString(f.Name)+"="+br.ReadInt32());}} }
 return;
}
var tools = Path.GetFullPath("work/tools/Cpp2IL_net472");
System.Runtime.Loader.AssemblyLoadContext.Default.Resolving += (ctx,n) => {
 var p=Path.Combine(tools,n.Name+".dll"); return File.Exists(p)?ctx.LoadFromAssemblyPath(p):null;
};
new Cpp2IlCorePlugin().OnLoad();
var root=@"D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo";
Cpp2IlApi.InitializeLibCpp2Il(Path.Combine(root,"GameAssembly.dll"),Path.GetFullPath("outputs/STARHOME_Localization_0.2.0/backup_original/StarHome_Data/il2cpp_data/Metadata/global-metadata.dat"),UnityVersion.Parse("6000.3.15f1"));
var app=Cpp2IlApi.CurrentAppContext!;
var names=new[]{"Gameplay.ResourceConfigData","Gameplay.ResourceManager","Gameplay.UI.ResourceRowView","Gameplay.UI.PriceItemView","Enums+Resources","Actions.Action","Actions.Sections","Actions.Section","Actions.WaitForTaskFocus","Gameplay.UI.TaskRowFactory","Gameplay.UI.TaskPanel","SerializableObject","SerializableObjectExtensions","GuidString","GuidStringExtensions"};
var methods=app.AllTypes.SelectMany(t=>t.Methods).Where(m=>m.UnderlyingPointer!=0).GroupBy(m=>m.UnderlyingPointer).ToDictionary(g=>g.Key,g=>string.Join(" | ",g.Take(3).Select(m=>m.FullName))+(g.Count()>3?" ...":""));
var output=new List<object>();
foreach(var t in app.AllTypes.Where(t=>names.Contains(t.FullName)||t.FullName.StartsWith("Actions.Sections+"))) {
 var mr=new List<object>();
 foreach(var m in t.Methods) {
  var instructions=new List<string>();
  if(m.UnderlyingPointer!=0 && (args.Contains("all") || t.FullName=="Gameplay.UI.TaskRowFactory" || m.Name.Contains("Name") || m.Name.Contains("Description") || m.Name.Contains("Find") || m.Name.Contains("ByName"))) {
   var bytes=m.RawBytes.ToArray();var decoder=Decoder.Create(64,new ByteArrayCodeReader(bytes));decoder.IP=m.UnderlyingPointer;
   var formatter=new IntelFormatter();var so=new StringOutput();
   while(decoder.IP<m.UnderlyingPointer+(ulong)bytes.Length) { decoder.Decode(out var ins);so.Reset();formatter.Format(ins,so);
    var note="";if(ins.FlowControl is FlowControl.Call or FlowControl.UnconditionalBranch && ins.NearBranchTarget!=0 && methods.TryGetValue(ins.NearBranchTarget,out var name))note=" ; "+name;
    instructions.Add($"{ins.IP:X16} {so}"+note);
   }
  }
  mr.Add(new{name=m.FullNameWithSignature,address=$"0x{m.UnderlyingPointer:X}",rva=$"0x{m.Rva:X}",instructions});
 }
 output.Add(new{name=t.FullName,fields=t.Fields.Select(f=>new{name=f.Name,type=f.FieldType.FullName}).ToArray(),methods=mr});
}
File.WriteAllText("work/expanded_021/native_resource.json",JsonSerializer.Serialize(output,new JsonSerializerOptions{WriteIndented=true}));
Console.WriteLine("Wrote task method evidence");



