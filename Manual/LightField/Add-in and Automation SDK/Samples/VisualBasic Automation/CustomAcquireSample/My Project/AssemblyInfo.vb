Imports System
Imports System.Reflection
Imports System.Runtime.InteropServices
Imports System.Globalization
Imports System.Resources
Imports System.Windows

' General Information about an assembly is controlled through the following 
' set of attributes. Change these attribute values to modify the information
' associated with an assembly.

' Review the values of the assembly attributes

<Assembly: AssemblyTitle("LightField VB Automation Sample")> 
<Assembly: AssemblyDescription("LightField VB Automation Sample")> 
<Assembly: AssemblyCompany("Teledyne Princeton Instruments")> 
<Assembly: AssemblyProduct("LightFieldVisualBasicAutomationSample")> 
<Assembly: AssemblyCopyright("Copyright © Teledyne Princeton Instruments 2013-2019")> 
<Assembly: AssemblyTrademark("")> 
<Assembly: ComVisible(false)>

'In order to begin building localizable applications, set 
'<UICulture>CultureYouAreCodingWith</UICulture> in your .vbproj file
'inside a <PropertyGroup>.  For example, if you are using US english 
'in your source files, set the <UICulture> to "en-US".  Then uncomment the
'NeutralResourceLanguage attribute below.  Update the "en-US" in the line
'below to match the UICulture setting in the project file.

'<Assembly: NeutralResourcesLanguage("en-US", UltimateResourceFallbackLocation.Satellite)> 


'The ThemeInfo attribute describes where any theme specific and generic resource dictionaries can be found.
'1st parameter: where theme specific resource dictionaries are located
'(used if a resource is not found in the page, 
' or application resource dictionaries)

'2nd parameter: where the generic resource dictionary is located
'(used if a resource is not found in the page, 
'app, and any theme specific resource dictionaries)
<Assembly: ThemeInfo(ResourceDictionaryLocation.None, ResourceDictionaryLocation.SourceAssembly)>



'The following GUID is for the ID of the typelib if this project is exposed to COM
<Assembly: Guid("3c17f7fd-158a-4c34-b7cd-1b6a77810924")> 

' - version information for an assembly consists of the following four values:
'      major version - major features
'      minor version - minor features
'      build number  - increments every distribution per like major and minor versions
'      revision      - 0 for beta; otherwise YYMM for date of distribution
' - file version:
'      assembly version for tech support
'      updates per distribution
' - assembly version:
'      version for clr
'      updates only when backwards compatibility is broken
'      revision is always zero by .NET convention
<Assembly: AssemblyFileVersion("5.0.0.1804")> 
<Assembly: AssemblyVersion("5.0.0.0")> 
