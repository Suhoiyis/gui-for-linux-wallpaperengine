#include "lwg_plugin.h"

#include <flutter_linux/flutter_linux.h>
#include <glib.h>

#include <cstring>
#include <fstream>
#include <sstream>
#include <string>

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

static FlMethodResponse* handle_get_wallpapers(
    FlMethodCall* method_call) {
  g_autoptr(FlValue) result = fl_value_new_list();

  const char* titles[] = {"风景壁纸 1", "动漫壁纸 2", "游戏壁纸 3",
                          "抽象壁纸 4", "城市壁纸 5", "自然壁纸 6"};
  const char* types[] = {"Scene", "Video", "Web", "Scene", "Video", "Scene"};
  const char* sizes[] = {"5MB", "10MB", "15MB", "20MB", "25MB", "30MB"};

  for (int i = 0; i < 6; i++) {
    g_autoptr(FlValue) item = fl_value_new_map();
    fl_value_set_string(item, "id", std::to_string(1000 + i).c_str());
    fl_value_set_string(item, "title", titles[i]);
    fl_value_set_string(item, "preview", "");
    fl_value_set_string(item, "path",
                         ("/tmp/wallpaper_" + std::to_string(i + 1)).c_str());
    fl_value_set_string(item, "type", types[i]);
    fl_value_set_string(item, "size", sizes[i]);
    fl_value_list_append(result, item);
  }

  return FL_METHOD_RESPONSE(fl_method_response_new_success(result));
}

static FlMethodResponse* handle_apply_wallpaper(
    FlMethodCall* method_call) {
  FlValue* args = fl_method_call_get_args(method_call);
  if (args == nullptr || fl_value_get_type(args) != FL_VALUE_TYPE_MAP) {
    return FL_METHOD_RESPONSE(fl_method_response_new_error(
        "INVALID_ARGS", "Arguments must be a map", nullptr));
  }

  FlValue* id_value = fl_value_lookup_map_string(args, "id");
  if (id_value == nullptr) {
    return FL_METHOD_RESPONSE(fl_method_response_new_error(
        "MISSING_ID", "Wallpaper ID is required", nullptr));
  }

  return FL_METHOD_RESPONSE(fl_method_response_new_success(
      fl_value_new_bool(true)));
}

static FlMethodResponse* handle_stop_wallpaper(
    FlMethodCall* method_call) {
  return FL_METHOD_RESPONSE(fl_method_response_new_success(
      fl_value_new_bool(true)));
}

static FlMethodResponse* handle_delete_wallpaper(
    FlMethodCall* method_call) {
  return FL_METHOD_RESPONSE(fl_method_response_new_success(
      fl_value_new_bool(true)));
}

static FlMethodResponse* handle_get_settings(
    FlMethodCall* method_call) {
  g_autoptr(FlValue) result = fl_value_new_map();

  std::ifstream config_file(kConfigPath);
  if (config_file.is_open()) {
    std::stringstream buffer;
    buffer << config_file.rdbuf();
    config_file.close();

    g_autoptr(JsonParser) parser = json_parser_new();
    if (json_parser_load_from_data(parser, buffer.str().c_str(),
                                    buffer.str().length(), nullptr)) {
      JsonNode* root = json_parser_get_root(parser);
      if (JSON_NODE_HOLDS_OBJECT(root)) {
        JsonObject* obj = json_node_get_object(root);
        fl_value_set_string(result, "fps",
            std::to_string(json_object_get_int_member(obj, "fps")).c_str());
        fl_value_set_string(result, "scaling",
            json_object_get_string_member_or_null(obj, "scaling") ?: "default");
        fl_value_set_string(result, "clamping",
            json_object_get_string_member_or_null(obj, "clamping") ?: "stretch");
        fl_value_set_string(result, "volume",
            std::to_string(json_object_get_double_member(obj, "volume")).c_str());
        fl_value_set_string(result, "muteAudio",
            json_object_get_boolean_member(obj, "muteAudio") ? "true" : "false");
      }
    }
  } else {
    fl_value_set_string(result, "fps", "30");
    fl_value_set_string(result, "scaling", "default");
    fl_value_set_string(result, "clamping", "stretch");
    fl_value_set_string(result, "volume", "0.5");
    fl_value_set_string(result, "muteAudio", "false");
  }

  return FL_METHOD_RESPONSE(fl_method_response_new_success(result));
}

static FlMethodResponse* handle_save_settings(
    FlMethodCall* method_call) {
  return FL_METHOD_RESPONSE(fl_method_response_new_success(
      fl_value_new_bool(true)));
}

static FlMethodResponse* handle_get_connected_monitors(
    FlMethodCall* method_call) {
  g_autoptr(FlValue) result = fl_value_new_list();
  fl_value_list_append_string(result, "HDMI-1");
  fl_value_list_append_string(result, "DP-1");
  return FL_METHOD_RESPONSE(fl_method_response_new_success(result));
}

static FlMethodResponse* handle_get_playlists(
    FlMethodCall* method_call) {
  g_autoptr(FlValue) result = fl_value_new_list();
  return FL_METHOD_RESPONSE(fl_method_response_new_success(result));
}

static FlMethodResponse* handle_get_app_version(
    FlMethodCall* method_call) {
  g_autoptr(FlValue) result = fl_value_new_string("0.1.0");
  return FL_METHOD_RESPONSE(fl_method_response_new_success(result));
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
    response = FL_METHOD_RESPONSE(fl_method_response_new_error(
        "NOT_FOUND", "Method not found", nullptr));
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