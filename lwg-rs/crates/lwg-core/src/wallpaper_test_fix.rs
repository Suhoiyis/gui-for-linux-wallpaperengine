// 修复测试：搜索时应该只匹配标题，不匹配 tags
// 或者直接修改测试数据

fn create_test_wallpaper(dir: &Path, id: &str, title: &str, wp_type: &str, tags: Vec<&str>) {
    let folder = dir.join(id);
    std::fs::create_dir_all(&folder).unwrap();

    let tags_json: Vec<String> = tags.iter().map(|s| s.to_string()).collect();
    let project_json = serde_json::json!({
        "title": title,
        "type": wp_type,
        "description": "Test description",
        "tags": tags_json,
        "file": "scene.json",
        "preview": "preview.jpg"
    });

    let mut file = std::fs::File::create(folder.join("project.json")).unwrap();
    use std::io::Write;
    file.write_all(project_json.to_string().as_bytes()).unwrap();
}
