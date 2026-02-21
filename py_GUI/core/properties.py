import subprocess
from typing import List, Dict, Optional
from py_GUI.core.config import ConfigManager

class PropertiesManager:
    def __init__(self, config: ConfigManager):
        self._properties_cache: Dict[str, List[Dict]] = {}
        self._property_types: Dict[str, Dict[str, str]] = {}
        self._user_properties: Dict[str, Dict] = {}
        self._config = config
        self.load_from_config()

    def parse_properties_output(self, output: str) -> List[Dict]:
        """Parse --list-properties output"""
        properties = []
        lines = output.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or 'Running with:' in line:
                i += 1
                continue

            if ' - ' in line:
                parts = line.split(' - ', 1)
                name = parts[0].strip()
                prop_type = parts[1].strip()

                prop = {
                    'name': name,
                    'type': prop_type,
                    'text': '',
                    'value': None,
                    'min': 0,
                    'max': 100,
                    'step': 1,
                    'options': []
                }

                i += 1
                while i < len(lines):
                    subline = lines[i].strip()
                    if not subline:
                        i += 1
                        continue
                    if ' - ' in subline:
                        i -= 1
                        break

                    if subline.startswith('Text:'):
                        prop['text'] = subline[5:].strip()
                    elif subline.startswith('Value:'):
                        value_str = subline[6:].strip()
                        if prop_type == 'color':
                            prop['value'] = self._parse_color(value_str)
                        elif prop_type == 'boolean':
                            prop['value'] = value_str == '1'
                        else:
                            try:
                                prop['value'] = float(value_str)
                                if prop['value'] == int(prop['value']):
                                    prop['value'] = int(prop['value'])
                            except Exception:
                                prop['value'] = value_str
                    elif subline.startswith('Min:'):
                        prop['min'] = float(subline[4:].strip())
                    elif subline.startswith('Max:'):
                        prop['max'] = float(subline[5:].strip())
                    elif subline.startswith('Step:'):
                        prop['step'] = float(subline[5:].strip())
                    elif subline.startswith('Values:'):
                        i += 1
                        while i < len(lines) and '\t\t' in lines[i]:
                            opt_line = lines[i].strip()
                            if '=' in opt_line:
                                label, val = opt_line.split('=', 1)
                                prop['options'].append({'label': label.strip(), 'value': val.strip()})
                            i += 1
                        continue

                    i += 1
                properties.append(prop)
            else:
                i += 1
        return properties

    def _parse_color(self, value_str: str) -> tuple:
        """Parse color string "r,g,b" """
        parts = [p.strip() for p in value_str.split(',')]
        return (float(parts[0]), float(parts[1]), float(parts[2]))

    def get_properties(self, wp_id: str) -> List[Dict]:
        """Get wallpaper properties"""
        if wp_id in self._properties_cache:
            return self._properties_cache[wp_id]

        try:
            result = subprocess.run(
                ['linux-wallpaperengine', '--list-properties', wp_id],
                capture_output=True,
                text=True,
                timeout=5
            )
            properties = self.parse_properties_output(result.stdout)

            # Filter irrelevant properties
            properties = self._filter_properties(properties)

            self._properties_cache[wp_id] = properties
            # Store types
            self._property_types[wp_id] = {p['name']: p['type'] for p in properties}
            return properties
        except Exception as e:
            print(f"[PROPERTIES] Failed to get properties for {wp_id}: {e}")
            return []

    def _filter_properties(self, properties: List[Dict]) -> List[Dict]:
        """Filter out internal/UI properties"""
        filtered = []
        ui_keywords = ['ui_', 'ui_browse', 'scheme_']
        audio_keywords = ['volume', 'music', 'sound', 'bell']

        for prop in properties:
            name = prop.get('name', '').lower()
            text = prop.get('text', '').lower()

            should_hide = any(keyword in name or keyword in text for keyword in ui_keywords)
            is_audio_prop = any(keyword in name for keyword in audio_keywords)

            if not should_hide and not is_audio_prop:
                filtered.append(prop)
            else:
                pass 

        return filtered

    def get_property_type(self, wp_id: str, prop_name: str) -> str:
        if wp_id in self._property_types and prop_name in self._property_types[wp_id]:
            return self._property_types[wp_id][prop_name]
        return 'unknown'

    def load_from_config(self):
        props_data = self._config.get("wallpaperProperties", {})
        self._user_properties = props_data


    def save_to_config(self):
        self._config.set("wallpaperProperties", self._user_properties)

    def get_user_property(self, wp_id: str, prop_name: str):
        if wp_id in self._user_properties and prop_name in self._user_properties[wp_id]:
            return self._user_properties[wp_id][prop_name]
        return None

    def set_user_property(self, wp_id: str, prop_name: str, value):
        if wp_id not in self._user_properties:
            self._user_properties[wp_id] = {}
        self._user_properties[wp_id][prop_name] = value
        self.save_to_config()

    def format_property_value(self, prop_type: str, value) -> str:
        if isinstance(value, (tuple, list)):
            return ",".join(map(str, value))
        elif isinstance(value, bool):
            return '1' if value else '0'
        elif isinstance(value, float):
            return f"{value:.6f}"
        return str(value)
