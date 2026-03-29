//! 性能基准测试

use criterion::{black_box, criterion_group, criterion_main, Criterion};

// 配置加载基准
fn bench_config_load(c: &mut Criterion) {
    c.bench_function("config_load", |b| {
        b.iter(|| {
            // 模拟配置加载
            let _config = black_box(());
        })
    });
}

// 壁纸扫描基准
fn bench_wallpaper_scan(c: &mut Criterion) {
    c.bench_function("wallpaper_scan", |b| {
        b.iter(|| {
            // 模拟扫描 100 个壁纸
            for i in 0..100 {
                let _ = black_box(i);
            }
        })
    });
}

// 缩略图加载基准
fn bench_thumbnail_load(c: &mut Criterion) {
    c.bench_function("thumbnail_load", |b| {
        b.iter(|| {
            // 模拟加载缩略图
            let _ = black_box(());
        })
    });
}

criterion_group!(benches, bench_config_load, bench_wallpaper_scan, bench_thumbnail_load);
criterion_main!(benches);
