import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/theme/app_theme.dart';

class WelcomeDialog extends ConsumerStatefulWidget {
  const WelcomeDialog({super.key});

  @override
  ConsumerState<WelcomeDialog> createState() => _WelcomeDialogState();
}

class _WelcomeDialogState extends ConsumerState<WelcomeDialog> {
  int _step = 0;
  final _pageController = PageController();

  static const _steps = [
    StepData(title: '欢迎', icon: Icons.waving_hand_outlined, content: '欢迎使用 Wallpaper Manager\n\n这是一个 Linux 壁纸引擎管理器\n帮助你管理和播放 Steam Workshop 壁纸'),
    StepData(title: '系统要求', icon: Icons.checklist_outlined, content: '需要以下组件:\n\n• linux-wallpaperengine (C++引擎)\n• Steam Workshop 壁纸资源\n• X11 或 Wayland 显示服务器'),
    StepData(title: '目录配置', icon: Icons.folder_outlined, content: '壁纸目录:\n\n默认从 Steam Workshop 目录扫描\n你可以在设置中自定义路径\n\n引擎将自动检测可用壁纸'),
    StepData(title: '快速设置', icon: Icons.speed_outlined, content: '推荐初始设置:\n\n• FPS: 30 (平衡性能和质量)\n• 音量: 50% (默认)\n• 缩放: 适应屏幕\n\n这些可以在设置页面随时调整'),
    StepData(title: '准备好了!', icon: Icons.celebration_outlined, content: '一切就绪!\n\n现在可以:\n• 浏览壁纸库\n• 应用喜欢的壁纸\n• 自定义设置\n• 使用 Ctrl+K 打开命令面板'),
  ];

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: AppTheme.surface,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: SizedBox(
        width: 600,
        height: 480,
        child: Column(
          children: [
            _buildHeader(),
            Expanded(child: _buildPageView()),
            _buildFooter(),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          ...List.generate(
            _steps.length,
            (i) => Padding(
              padding: const EdgeInsets.only(right: 8),
              child: Container(
                width: 10,
                height: 10,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: i <= _step ? AppTheme.primary : Colors.white.withValues(alpha: 0.2),
                ),
              ),
            ),
          ),
          const Spacer(),
          Text(
            _steps[_step].title,
            style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w600),
          ),
        ],
      ),
    );
  }

  Widget _buildPageView() {
    return PageView.builder(
      controller: _pageController,
      itemCount: _steps.length,
      physics: const NeverScrollableScrollPhysics(),
      itemBuilder: (context, index) {
        final step = _steps[index];
        return Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: AppTheme.primaryGradient,
                  boxShadow: [BoxShadow(color: AppTheme.primary.withValues(alpha: 0.3), blurRadius: 20)],
                ),
                child: Icon(step.icon, color: Colors.white, size: 48),
              ),
              const SizedBox(height: 24),
              Text(
                step.content,
                style: const TextStyle(color: Colors.white70, fontSize: 14),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildFooter() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          if (_step > 0)
            OutlinedButton(
              onPressed: _goBack,
              style: OutlinedButton.styleFrom(
                foregroundColor: AppTheme.textSecondary,
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
              child: const Text('上一步'),
            ),
          const Spacer(),
          ElevatedButton(
            onPressed: _step == _steps.length - 1 ? _complete : _goNext,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primary,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
            child: Text(_step == _steps.length - 1 ? '开始使用' : '下一步'),
          ),
        ],
      ),
    );
  }

  void _goNext() {
    setState(() => _step++);
    _pageController.nextPage(duration: const Duration(milliseconds: 300), curve: Curves.easeOut);
  }

  void _goBack() {
    setState(() => _step--);
    _pageController.previousPage(duration: const Duration(milliseconds: 300), curve: Curves.easeOut);
  }

  void _complete() {
    Navigator.of(context).pop();
  }
}

class StepData {
  final String title;
  final IconData icon;
  final String content;

  const StepData({required this.title, required this.icon, required this.content});
}

void showWelcomeDialog(BuildContext context) {
  showDialog(
    context: context,
    barrierDismissible: false,
    builder: (context) => const WelcomeDialog(),
  );
}