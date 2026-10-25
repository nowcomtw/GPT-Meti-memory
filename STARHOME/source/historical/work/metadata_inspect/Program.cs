using System.Reflection;
using System.Text.Json;
using LibCpp2IL;
using AssetRipper.Primitives;

var root = @"D:\Program Files (x86)\Steam\steamapps\common\STARHOME Demo";
var tools = Path.GetFullPath("work/tools/Cpp2IL_net472");
System.Runtime.Loader.AssemblyLoadContext.Default.Resolving += (ctx, n) => {
    var p = Path.Combine(tools, n.Name + ".dll");
    return File.Exists(p) ? ctx.LoadFromAssemblyPath(p) : null;
};
if (!LibCpp2IlMain.LoadFromFile(Path.Combine(root,"GameAssembly.dll"),Path.Combine(root,"StarHome_Data/il2cpp_data/Metadata/global-metadata.dat"),UnityVersion.Parse("6000.3.15f1")))
    throw new Exception("Metadata load failed");
var rows = new List<object>();
File.WriteAllText("work/prototype_evidence/type_assembly_map.json",JsonSerializer.Serialize(LibCpp2IlMain.TheMetadata!.typeDefs.Select(t=>new {name=t.FullName,assembly=t.DeclaringAssembly?.Name})));
foreach (var t in LibCpp2IlMain.TheMetadata!.typeDefs) {
    if (!(t.Namespace?.StartsWith("Gameplay") == true || t.Namespace?.StartsWith("Events") == true || t.Namespace?.StartsWith("Actions") == true || t.Namespace?.StartsWith("Conditions") == true || t.FullName?.Contains("UxmlSerializedData") == true || t.FullName?.StartsWith("UnityEngine.UIElements.VisualTreeAsset") == true || t.FullName?.StartsWith("UnityEngine.TextCore.Text.FontAsset") == true)) continue;
    try {
        var fields = t.Fields?.Select(f => new {name=f.Name, type=f.FieldType?.ToString(), attributes=f.RawFieldType?.Attrs, token=$"0x{f.token:x8}"}).ToArray();
        rows.Add(new {name=t.FullName, assembly=t.DeclaringAssembly?.Name, baseType=t.BaseType?.ToString(), fields});
    } catch (Exception e) { rows.Add(new {name=t.FullName,error=e.Message}); }
}
File.WriteAllText("work/analysis/type_fields.json",JsonSerializer.Serialize(rows,new JsonSerializerOptions{WriteIndented=true}));
Console.WriteLine($"Wrote {rows.Count} type definitions");
