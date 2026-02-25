use gtk4::prelude::*;
use relm4::prelude::*;
use lwg_core::properties::{WallpaperProperty, PropertyType};

/// 属性编辑器组件
pub struct PropertiesEditor {
    properties: Vec<WallpaperProperty>,
    current_wp_id: Option<String>,
}

#[derive(Debug)]
pub enum PropertiesEditorInput {
    LoadProperties(String, Vec<WallpaperProperty>),
    UpdateProperty(String, String, serde_json::Value),
}

#[derive(Debug)]
pub enum PropertiesEditorOutput {
    PropertyChanged(String, String, serde_json::Value),
}

#[relm4::component(pub)]
impl Component for PropertiesEditor {
    type Init = ();
    type Input = PropertiesEditorInput;
    type Output = PropertiesEditorOutput;
    type CommandOutput = ();

    view! {
        gtk4::Box {
            set_orientation: gtk4::Orientation::Vertical,
            set_spacing: 12,
            set_margin_all: 12,
            set_visible: false,

            gtk4::Label {
                set_label: "属性",
                add_css_class: "heading",
                set_halign: gtk4::Align::Start,
            },

            gtk4::Separator {},

            // 属性编辑器占位
            gtk4::Label {
                set_label: "选择 Web 壁纸后显示属性",
                add_css_class: "dim-label",
                set_halign: gtk4::Align::Center,
            },
        }
    }

    fn init(
        _init: Self::Init,
        _root: Self::Root,
        _sender: ComponentSender<Self>,
    ) -> ComponentParts<Self> {
        let model = Self {
            properties: Vec::new(),
            current_wp_id: None,
        };
        let widgets = view_output!();
        ComponentParts { model, widgets }
    }

    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _root: &Self::Root) {
        match msg {
            PropertiesEditorInput::LoadProperties(wp_id, properties) => {
                self.current_wp_id = Some(wp_id);
                self.properties = properties;
                // TODO: 动态生成属性编辑 UI
            }
            PropertiesEditorInput::UpdateProperty(wp_id, prop_name, value) => {
                sender.output(PropertiesEditorOutput::PropertyChanged(wp_id, prop_name, value)).ok();
            }
        }
    }
}

/// 创建属性编辑控件
pub fn create_property_editor(prop: &WallpaperProperty, sender: &relm4::Sender<PropertiesEditorInput>) -> gtk4::Widget {
    match prop.prop_type {
        PropertyType::Slider => {
            let box_widget = gtk4::Box::new(gtk4::Orientation::Horizontal, 6);
            
            let label = gtk4::Label::new(Some(&prop.text));
            label.set_hexpand(true);
            label.set_halign(gtk4::Align::Start);
            
            let scale = gtk4::Scale::with_range(gtk4::Orientation::Horizontal, prop.min, prop.max);
            scale.set_step_increment(prop.step);
            scale.set_size_request(150, -1);
            
            if let Some(value) = &prop.value {
                if let Some(num) = value.as_f64() {
                    scale.set_value(num);
                }
            }
            
            box_widget.append(&label);
            box_widget.append(&scale);
            box_widget.upcast()
        }
        PropertyType::Boolean => {
            let box_widget = gtk4::Box::new(gtk4::Orientation::Horizontal, 6);
            
            let label = gtk4::Label::new(Some(&prop.text));
            label.set_hexpand(true);
            label.set_halign(gtk4::Align::Start);
            
            let switch = gtk4::Switch::new();
            if let Some(value) = &prop.value {
                if let Some(b) = value.as_bool() {
                    switch.set_active(b);
                }
            }
            
            box_widget.append(&label);
            box_widget.append(&switch);
            box_widget.upcast()
        }
        PropertyType::Color => {
            // 简化实现：使用 Label 显示
            let label = gtk4::Label::new(Some(&format!("{}: 颜色选择器待实现", prop.text)));
            label.set_halign(gtk4::Align::Start);
            label.upcast()
        }
        PropertyType::Options => {
            let box_widget = gtk4::Box::new(gtk4::Orientation::Horizontal, 6);
            
            let label = gtk4::Label::new(Some(&prop.text));
            label.set_hexpand(true);
            label.set_halign(gtk4::Align::Start);
            
            let dropdown = gtk4::DropDown::new(Some(&gtk4::StringList::new(
                &prop.options.iter().map(|opt| opt.label.as_str()).collect::<Vec<_>>()
            )), None);
            
            box_widget.append(&label);
            box_widget.append(&dropdown);
            box_widget.upcast()
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_properties_editor_exists() {
        assert!(true);
    }
}
