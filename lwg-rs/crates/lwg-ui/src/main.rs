use relm4::prelude::*;
use lwg_ui::App;

fn main() {
    let app = RelmApp::new("com.wallpaperengine.gui");
    app.run::<App>(0);
}
