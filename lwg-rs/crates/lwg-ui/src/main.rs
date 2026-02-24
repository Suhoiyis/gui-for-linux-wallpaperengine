use gtk4::prelude::*;
use relm4::prelude::*;

mod app;
use app::{App, AppMsg};

fn main() {
    let app = RelmApp::new("com.wallpaperengine.gui");
    app.run::<App>(());
}