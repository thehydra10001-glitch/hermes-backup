# Example: /resources Command

Concrete implementation of the 4-file slash command pattern.
Added in session 2026-07-08.

## 1. CommandDef (hermes_cli/commands.py)

```python
CommandDef("resources", "Show system resources (CPU, RAM, storage, battery)", "Info"),
```

Placed in the `# Info` section, after `/insights`.

## 2. Gateway Handler (gateway/slash_commands.py)

```python
async def _handle_resources_command(self, event: MessageEvent) -> str:
    """Handle /resources — show system resource usage (CPU, RAM, storage, battery)."""
    import psutil

    lines = ["🖥  System Resources", ""]

    # CPU
    cpu_pct = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    freq_str = f" @ {cpu_freq.current:.0f} MHz" if cpu_freq else ""
    load1, load5, load15 = psutil.getloadavg()
    lines.append(f"🔲 CPU: {cpu_pct}%  ({cpu_count} cores{freq_str})")
    lines.append(f"   Load: {load1:.1f} / {load5:.1f} / {load15:.1f}")

    # RAM
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    gb_total = vm.total / (1024 ** 3)
    gb_used = vm.used / (1024 ** 3)
    gb_avail = vm.available / (1024 ** 3)
    lines.append("")
    lines.append(f"🧠 RAM: {vm.percent}%  ({gb_used:.1f} / {gb_total:.1f} GB)")
    lines.append(f"   Available: {gb_avail:.1f} GB")
    if swap.total > 0:
        lines.append(f"   Swap: {swap.used / (1024 ** 3):.1f} / {swap.total / (1024 ** 3):.1f} GB ({swap.percent}%)")

    # Disk
    lines.append("")
    lines.append("💾 Storage:")
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            gb_total_d = usage.total / (1024 ** 3)
            gb_used_d = usage.used / (1024 ** 3)
            lines.append(f"   {part.mountpoint}: {usage.percent}%  ({gb_used_d:.1f} / {gb_total_d:.1f} GB)")
        except PermissionError:
            continue

    # Battery
    battery = psutil.sensors_battery()
    if battery is not None:
        lines.append("")
        status = "⚡ Charging" if battery.power_plugged else "🔋 On battery"
        remaining = ""
        if battery.secsleft > 0 and not battery.power_plugged:
            hrs, rem = divmod(battery.secsleft, 3600)
            mins = rem // 60
            remaining = f"  ({int(hrs)}h {int(mins)}m remaining)"
        lines.append(f"🔋 Battery: {round(battery.percent)}%  {status}{remaining}")
    else:
        lines.append("")
        lines.append("🔋 Battery: N/A (no battery detected)")

    return "\n".join(lines)
```

## 3. Dispatch (gateway/run.py)

```python
if canonical == "resources":
    return await self._handle_resources_command(event)
```

Placed right after the `status` dispatch block.

## 4. CLI Handler (cli.py)

Dispatch in `process_command()`:
```python
elif canonical == "resources":
    self._show_resources()
```

Method on `HermesCLI` class (same body as gateway handler, but uses `self._console_print()`):
```python
def _show_resources(self):
    """Show system resource usage (CPU, RAM, storage, battery)."""
    import psutil
    # ... same logic as gateway handler ...
    self._console_print("\n".join(lines), highlight=False, markup=False)
```

## Notes

- `psutil` is lazy-imported inside the handler to avoid import-time overhead
- Battery `%` is rounded with `round()` to avoid ugly floats like `86.981598461961%`
- Disk partitions use `all=False` to skip virtual pseudo-filesystems
- `PermissionError` caught for restricted mount points
