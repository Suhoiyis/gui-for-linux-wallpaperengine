#include "lwg_plugin.h"

#include <flutter_linux/flutter_linux.h>
#include <glib.h>
#include <dirent.h>
#include <sys/stat.h>

#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

static constexpr char kChannelName[] = "lwg_gui/platform";

static constexpr char kGetWallpapers[] = "get_wallpapers";
static constexpr char kApplyWallpaper[] = "apply_wallpaper";
static constexpr char kStopWallpaper[] = "stop_wallpaper";
static constexpr char kDeleteWallpaper[] = "delete_wallpaper";
static constexpr char kGetSettings[] = "get_settings";
static constexpr char kSaveSettings[] = "save_settings";
static constexpr char kGetConnectedMonitors[] = "get_connected_monitors";
static constexpr char kGetPlaylists[] = "get_playlists";
static constexpr char kGetAppVersion[] = "get_app_version";

static const std::string kConfigPath =
    std::string(g_get_user_config_dir()) +
    "/linux-wallpaperengine-gui/config.json";

static const std::string kDefaultWorkshopPath =
    std::string(g_get_home_dir()) +
    "/.local/share/Steam/steamapps/workshop/content/431960";

static std::string get_workshop_path() {
  // Check config for custom workshop_path
  std::ifstream config_file(kConfigPath);
  if (config_file.is_open()) {
    std::stringstream buffer;
    buffer << config_file.rdbuf();
    config_file.close();
    std::string content = buffer.str();
    // Simple search for "workshopPath" in JSON
    size_t pos = content.find("\"workshopPath\"");
    if (pos != std::string::npos) {
      size_t colon = content.find(':', pos);
      if (colon != std::string::npos) {
        size_t quote1 = content.find('"', colon + 1);
        if (quote1 != std::string::npos) {
          size_t quote2 = content.find('"', quote1 + 1);
          if (quote2 != std::string::npos) {
            std::string path = content.substr(quote1 + 1, quote2 - quote1 - 1);
            if (!path.empty()) return path;
          }
        }
      }
    }
  }
  return kDefaultWorkshopPath;
}

static std::string get_folder_size(const std::string& path) {
  long total = 0;
  DIR* dir = opendir(path.c_str());
  if (dir == nullptr) return "0B";
  struct dirent* entry;
  while ((entry = readdir(dir)) != nullptr) {
    if (entry->d_name[0] == '.') continue;
    std::string full = path + "/" + entry->d_name;
    struct stat st;
    if (stat(full.c_str(), &st) == 0 && S_ISREG(st.st_mode)) {
      total += st.st_size;
    }
  }
  closedir(dir);
  if (total < 1024) return std::to_string(total) + "B";
  if (total < 1024 * 1024) return std::to_string(total / 1024) + "KB";
  return std::to_string(total / (1024 * 1024)) + "MB";
}

static FlMethodResponse* handle_get_wallpapers(
    FlMethodCall* method_call) {
  g_autoptr(FlValue) result = fl_value_new_list();

  std::string workshop_path = get_workshop_path();
  DIR* dir = opendir(workshop_path.c_str());
  if (dir == nullptr) {
    // Workshop not found — return empty list (Dart side will use mock fallback)
    return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
  }

  struct dirent* entry;
  while ((entry = readdir(dir)) != nullptr) {
    if (entry->d_name[0] == '.') continue;

    std::string folder = entry->d_name;
    std::string json_path = workshop_path + "/" + folder + "/project.json";

    std::ifstream jf(json_path);
    if (!jf.is_open()) continue;

    std::stringstream jb;
    jb << jf.rdbuf();
    jf.close();
    std::string json_content = jb.str();

    // Simple JSON field extraction (no json-glib dependency)
    auto extract_field = [&](const std::string& key, const std::string& def) -> std::string {
      std::string search = "\"" + key + "\"";
      size_t pos = json_content.find(search);
      if (pos == std::string::npos) return def;
      size_t colon = json_content.find(':', pos + search.length());
      if (colon == std::string::npos) return def;
      size_t quote1 = json_content.find('"', colon + 1);
      if (quote1 == std::string::npos) return def;
      size_t quote2 = json_content.find('"', quote1 + 1);
      if (quote2 == std::string::npos) return def;
      return json_content.substr(quote1 + 1, quote2 - quote1 - 1);
    };

    g_autoptr(FlValue) item = fl_value_new_map();
    fl_value_set_string_take(item, "id", fl_value_new_string(folder.c_str()));
    fl_value_set_string_take(item, "title", fl_value_new_string(extract_field("title", "Unknown").c_str()));

    std::string preview_file = extract_field("preview", "preview.jpg");
    std::string folder_path = workshop_path + "/" + folder;
    std::string preview_path = folder_path + "/" + preview_file;
    fl_value_set_string_take(item, "preview", fl_value_new_string(preview_path.c_str()));
    fl_value_set_string_take(item, "path", fl_value_new_string(folder_path.c_str()));

    std::string wtype = extract_field("type", "scene");
    std::string type_lower = wtype;
    for (auto& c : type_lower) c = tolower(c);
    fl_value_set_string_take(item, "type", fl_value_new_string(type_lower.c_str()));

    fl_value_set_string_take(item, "size", fl_value_new_string(get_folder_size(folder_path).c_str()));
    fl_value_set_string_take(item, "description", fl_value_new_string(extract_field("description", "").c_str()));
    fl_value_append_take(result, fl_value_ref(item));
  }
  closedir(dir);

  return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
}

static FlMethodResponse* handle_apply_wallpaper(
    FlMethodCall* method_call) {
  FlValue* args = fl_method_call_get_args(method_call);
  if (args == nullptr || fl_value_get_type(args) != FL_VALUE_TYPE_MAP) {
    return FL_METHOD_RESPONSE(fl_method_error_response_new(
        "INVALID_ARGS", "Arguments must be a map", nullptr));
  }

  FlValue* id_value = fl_value_lookup_string(args, "id");
  if (id_value == nullptr) {
    return FL_METHOD_RESPONSE(fl_method_error_response_new(
        "MISSING_ID", "Wallpaper ID is required", nullptr));
  }

  // TODO: spawn linux-wallpaperengine process
  return FL_METHOD_RESPONSE(
      fl_method_success_response_new(fl_value_new_bool(true)));
}

static FlMethodResponse* handle_stop_wallpaper(
    FlMethodCall* method_call) {
  // TODO: kill wallpaperengine process
  return FL_METHOD_RESPONSE(
      fl_method_success_response_new(fl_value_new_bool(true)));
}

static FlMethodResponse* handle_delete_wallpaper(
    FlMethodCall* method_call) {
  // TODO: delete wallpaper folder
  return FL_METHOD_RESPONSE(
      fl_method_success_response_new(fl_value_new_bool(true)));
}

static FlMethodResponse* handle_get_settings(
    FlMethodCall* method_call) {
  g_autoptr(FlValue) result = fl_value_new_map();

  std::ifstream config_file(kConfigPath);
  if (config_file.is_open()) {
    std::stringstream buffer;
    buffer << config_file.rdbuf();
    config_file.close();
    fl_value_set_string_take(result, "rawJson",
        fl_value_new_string(buffer.str().c_str()));
  } else {
    fl_value_set_string_take(result, "fps", fl_value_new_int(30));
    fl_value_set_string_take(result, "scaling",
        fl_value_new_string("default"));
    fl_value_set_string_take(result, "clamping",
        fl_value_new_string("stretch"));
    fl_value_set_string_take(result, "volume",
        fl_value_new_float(0.5));
    fl_value_set_string_take(result, "muteAudio",
        fl_value_new_bool(false));
  }

  return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
}

static FlMethodResponse* handle_save_settings(
    FlMethodCall* method_call) {
  // TODO: write settings to config.json
  return FL_METHOD_RESPONSE(
      fl_method_success_response_new(fl_value_new_bool(true)));
}

static FlMethodResponse* handle_get_connected_monitors(
    FlMethodCall* method_call) {
  // TODO: use xrandr or DRM to detect real monitors
  g_autoptr(FlValue) result = fl_value_new_list();
  const gchar* monitors[] = {"HDMI-1", "DP-1"};
  for (int i = 0; i < 2; i++) {
    fl_value_append_take(result, fl_value_new_string(monitors[i]));
  }
  return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
}

static FlMethodResponse* handle_get_playlists(
    FlMethodCall* method_call) {
  // TODO: read playlists from config
  g_autoptr(FlValue) result = fl_value_new_list();
  return FL_METHOD_RESPONSE(fl_method_success_response_new(result));
}

static FlMethodResponse* handle_get_app_version(
    FlMethodCall* method_call) {
  return FL_METHOD_RESPONSE(
      fl_method_success_response_new(fl_value_new_string("0.1.0")));
}

static void method_call_handler(FlMethodChannel* channel,
                                 FlMethodCall* method_call,
                                 gpointer user_data) {
  const gchar* method = fl_method_call_get_name(method_call);

  FlMethodResponse* response = nullptr;

  if (strcmp(method, kGetWallpapers) == 0) {
    response = handle_get_wallpapers(method_call);
  } else if (strcmp(method, kApplyWallpaper) == 0) {
    response = handle_apply_wallpaper(method_call);
  } else if (strcmp(method, kStopWallpaper) == 0) {
    response = handle_stop_wallpaper(method_call);
  } else if (strcmp(method, kDeleteWallpaper) == 0) {
    response = handle_delete_wallpaper(method_call);
  } else if (strcmp(method, kGetSettings) == 0) {
    response = handle_get_settings(method_call);
  } else if (strcmp(method, kSaveSettings) == 0) {
    response = handle_save_settings(method_call);
  } else if (strcmp(method, kGetConnectedMonitors) == 0) {
    response = handle_get_connected_monitors(method_call);
  } else if (strcmp(method, kGetPlaylists) == 0) {
    response = handle_get_playlists(method_call);
  } else if (strcmp(method, kGetAppVersion) == 0) {
    response = handle_get_app_version(method_call);
  } else {
    response = FL_METHOD_RESPONSE(fl_method_not_implemented_response_new());
  }

  fl_method_call_respond(method_call, response, nullptr);
}

void lwg_plugin_register_with_registrar(
    FlPluginRegistrar* registrar) {
  g_autoptr(FlStandardMethodCodec) codec = fl_standard_method_codec_new();
  g_autoptr(FlMethodChannel) channel =
      fl_method_channel_new(fl_plugin_registrar_get_messenger(registrar),
                            kChannelName, FL_METHOD_CODEC(codec));
  fl_method_channel_set_method_call_handler(channel, method_call_handler,
                                             nullptr, nullptr);
}