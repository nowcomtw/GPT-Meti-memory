using System.Text.Json;
using Cpp2IL.Core;
using Cpp2IL.Core.OutputFormats;
using AssetRipper.Primitives;

var tools = Path.GetFullPath("work/tools/Cpp2IL_net472");
System.Runtime.Loader.AssemblyLoadContext.Default.Resolving += (ctx,n) => {
 var p=Path.Combine(tools,n.Name+".dll"); return File.Exists(p)?ctx.LoadFromAssemblyPath(p):null;
};
new Cpp2IlCorePlugin().OnLoad();
var root=@"D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo";
Cpp2IlApi.InitializeLibCpp2Il(Path.Combine(root,"GameAssembly.dll"),Path.Combine(root,"StarHome_Data/il2cpp_data/Metadata/global-metadata.dat"),UnityVersion.Parse("6000.3.15f1"));
var app=Cpp2IlApi.CurrentAppContext!;
var removed=new List<object>();
var attrErrors=new List<object>();
foreach(var t in app.AllTypes) {
 try {t.AnalyzeCustomAttributeData();} catch(Exception e){attrErrors.Add(new {type=t.FullName,member="type",error=e.Message});}
 foreach(var f in t.Fields) {
  try {f.AnalyzeCustomAttributeData();} catch(Exception e){attrErrors.Add(new {type=t.FullName,member=f.Name,error=e.Message});}
 }
}
foreach(var t in app.AllTypes) {
 foreach(var p in t.Properties.ToArray()) {
  try { var pt=p.PropertyType; }
  catch(Exception e) { removed.Add(new {assembly=t.DeclaringAssembly.Name,type=t.Name,property=p.Name,error=e.GetType().Name});t.Properties.Remove(p); }
 }
}
Directory.CreateDirectory("work/prototype_evidence");
File.WriteAllText("work/prototype_evidence/dummy_export_exclusions.json",JsonSerializer.Serialize(removed,new JsonSerializerOptions{WriteIndented=true}));
File.WriteAllText("work/prototype_evidence/dummy_attribute_errors.json",JsonSerializer.Serialize(attrErrors,new JsonSerializerOptions{WriteIndented=true}));
Console.WriteLine($"Analyzed type and field attributes; {attrErrors.Count} failures recorded");
Console.WriteLine($"Removed {removed.Count} invalid properties from analysis model only");
new AsmResolverDllOutputFormatDefault().DoOutput(app,"work/prototype_evidence/dummy_dll");
Console.WriteLine("DUMMY_EXPORT_SUCCESS");
