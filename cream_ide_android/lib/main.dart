import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
  ));
  runApp(const CreamIDEApp());
}

// ── 15 Languages ──
const Map<String, Map<String, String>> kLang = {
  'English':    {'run':'Run','output':'Output','files':'Files','settings':'Settings','newfile':'New File','save':'Save','open':'Open','clear':'Clear','theme':'Theme','language':'Language','folder':'Project Folder','close':'Close','dark':'Dark','light':'Light','running':'Running...','done':'Done','nooutput':'Press Run to execute','highlight':'Syntax Highlighting'},
  'Русский':    {'run':'Запуск','output':'Вывод','files':'Файлы','settings':'Настройки','newfile':'Новый файл','save':'Сохранить','open':'Открыть','clear':'Очистить','theme':'Тема','language':'Язык','folder':'Папка проекта','close':'Закрыть','dark':'Тёмная','light':'Светлая','running':'Выполняется...','done':'Готово','nooutput':'Нажмите Run для запуска','highlight':'Подсветка синтаксиса'},
  'Español':    {'run':'Ejecutar','output':'Salida','files':'Archivos','settings':'Ajustes','newfile':'Nuevo','save':'Guardar','open':'Abrir','clear':'Limpiar','theme':'Tema','language':'Idioma','folder':'Carpeta','close':'Cerrar','dark':'Oscuro','light':'Claro','running':'Ejecutando...','done':'Listo','nooutput':'Presiona Run','highlight':'Resaltado'},
  'Français':   {'run':'Exécuter','output':'Sortie','files':'Fichiers','settings':'Paramètres','newfile':'Nouveau','save':'Sauvegarder','open':'Ouvrir','clear':'Effacer','theme':'Thème','language':'Langue','folder':'Dossier','close':'Fermer','dark':'Sombre','light':'Clair','running':'Exécution...','done':'Terminé','nooutput':'Appuyez sur Run','highlight':'Coloration'},
  'Deutsch':    {'run':'Ausführen','output':'Ausgabe','files':'Dateien','settings':'Einstellungen','newfile':'Neue Datei','save':'Speichern','open':'Öffnen','clear':'Löschen','theme':'Design','language':'Sprache','folder':'Projektordner','close':'Schließen','dark':'Dunkel','light':'Hell','running':'Wird ausgeführt...','done':'Fertig','nooutput':'Run drücken','highlight':'Syntaxhervorhebung'},
  '中文':        {'run':'运行','output':'输出','files':'文件','settings':'设置','newfile':'新文件','save':'保存','open':'打开','clear':'清除','theme':'主题','language':'语言','folder':'项目文件夹','close':'关闭','dark':'深色','light':'浅色','running':'运行中...','done':'完成','nooutput':'按运行执行代码','highlight':'语法高亮'},
  '日本語':      {'run':'実行','output':'出力','files':'ファイル','settings':'設定','newfile':'新規','save':'保存','open':'開く','clear':'クリア','theme':'テーマ','language':'言語','folder':'フォルダ','close':'閉じる','dark':'ダーク','light':'ライト','running':'実行中...','done':'完了','nooutput':'実行を押してください','highlight':'シンタックスハイライト'},
  '한국어':      {'run':'실행','output':'출력','files':'파일','settings':'설정','newfile':'새 파일','save':'저장','open':'열기','clear':'지우기','theme':'테마','language':'언어','folder':'폴더','close':'닫기','dark':'다크','light':'라이트','running':'실행 중...','done':'완료','nooutput':'Run을 눌러 실행','highlight':'구문 강조'},
  'Português':  {'run':'Executar','output':'Saída','files':'Arquivos','settings':'Configurações','newfile':'Novo','save':'Salvar','open':'Abrir','clear':'Limpar','theme':'Tema','language':'Idioma','folder':'Pasta','close':'Fechar','dark':'Escuro','light':'Claro','running':'Executando...','done':'Pronto','nooutput':'Pressione Run','highlight':'Realce'},
  'Italiano':   {'run':'Esegui','output':'Output','files':'File','settings':'Impostazioni','newfile':'Nuovo','save':'Salva','open':'Apri','clear':'Pulisci','theme':'Tema','language':'Lingua','folder':'Cartella','close':'Chiudi','dark':'Scuro','light':'Chiaro','running':'Esecuzione...','done':'Fatto','nooutput':'Premi Run','highlight':'Evidenziazione'},
  'Polski':     {'run':'Uruchom','output':'Wyjście','files':'Pliki','settings':'Ustawienia','newfile':'Nowy plik','save':'Zapisz','open':'Otwórz','clear':'Wyczyść','theme':'Motyw','language':'Język','folder':'Folder','close':'Zamknij','dark':'Ciemny','light':'Jasny','running':'Uruchamianie...','done':'Gotowe','nooutput':'Naciśnij Run','highlight':'Podświetlanie'},
  'Türkçe':     {'run':'Çalıştır','output':'Çıktı','files':'Dosyalar','settings':'Ayarlar','newfile':'Yeni','save':'Kaydet','open':'Aç','clear':'Temizle','theme':'Tema','language':'Dil','folder':'Klasör','close':'Kapat','dark':'Koyu','light':'Açık','running':'Çalışıyor...','done':'Tamam','nooutput':'Run\'a basın','highlight':'Sözdizimi'},
  'العربية':    {'run':'تشغيل','output':'مخرجات','files':'ملفات','settings':'إعدادات','newfile':'ملف جديد','save':'حفظ','open':'فتح','clear':'مسح','theme':'مظهر','language':'لغة','folder':'مجلد','close':'إغلاق','dark':'داكن','light':'فاتح','running':'جاري...','done':'تم','nooutput':'اضغط تشغيل','highlight':'تظليل'},
  'हिन्दी':     {'run':'चलाएं','output':'आउटपुट','files':'फ़ाइलें','settings':'सेटिंग्स','newfile':'नई फ़ाइल','save':'सहेजें','open':'खोलें','clear':'साफ़','theme':'थीम','language':'भाषा','folder':'फ़ोल्डर','close':'बंद','dark':'डार्क','light':'लाइट','running':'चल रहा है...','done':'हो गया','nooutput':'Run दबाएं','highlight':'हाइलाइट'},
  'Українська': {'run':'Запуск','output':'Вивід','files':'Файли','settings':'Налаштування','newfile':'Новий файл','save':'Зберегти','open':'Відкрити','clear':'Очистити','theme':'Тема','language':'Мова','folder':'Папка','close':'Закрити','dark':'Темна','light':'Світла','running':'Виконується...','done':'Готово','nooutput':'Натисніть Run','highlight':'Підсвічування'},
};

// ── Real Cream syntax examples ──
const Map<String, String> kSampleFiles = {
  'hello.cream': '''-- Hello World in Cream
name = "World"
say "Hello, {name}!"
say "Welcome to Cream programming language."''',

  'fizzbuzz.cream': '''-- FizzBuzz in Cream
for each i in range(1, 31)
    if i % 15 == 0
        say "FizzBuzz"
    else if i % 3 == 0
        say "Fizz"
    else if i % 5 == 0
        say "Buzz"
    else
        say i''',

  'fibonacci.cream': '''-- Fibonacci sequence
action fib(n)
    if n <= 1
        return n
    return fib(n - 1) + fib(n - 2)

repeat 10 with i
    say fib(i)''',

  'pipeline.cream': '''-- Pipeline operators
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

result = numbers
    | filter(x -> x % 2 == 0)
    | map(x -> x * 3)
    | sum

say "Result: {result}"''',

  'calculator.cream': '''-- Simple calculator
action calc(a, op, b)
    if op == "+"
        return a + b
    if op == "-"
        return a - b
    if op == "*"
        return a * b
    if op == "/"
        return a / b

say calc(10, "+", 5)
say calc(10, "*", 3)
say calc(20, "-", 8)''',
};

// ── Cream Syntax Highlighter ──
List<TextSpan> highlightCream(String text, bool isDark) {
  final Color cKw  = const Color(0xFFff6b9d);
  final Color cFn  = isDark ? const Color(0xFF79c0ff) : const Color(0xFF0550ae);
  final Color cStr = isDark ? const Color(0xFFa8ff78) : const Color(0xFF116329);
  final Color cNum = const Color(0xFFffab70);
  final Color cCmt = const Color(0xFF6a737d);
  final Color cOp  = const Color(0xFFff6b9d);
  final Color cDef = isDark ? const Color(0xFFc9d4e0) : const Color(0xFF24292e);
  final Color cPipe= const Color(0xFF00ffe0);

  const keywords = {
    'if','else','for','each','in','repeat','with','action',
    'return','struct','try','on','error','yes','no','and',
    'or','not','say','ask','import','from','as',
  };

  final spans = <TextSpan>[];
  final lines = text.split('\n');

  for (int li = 0; li < lines.length; li++) {
    final line = lines[li];
    int i = 0;

    // Full-line comment
    if (line.trimLeft().startsWith('--')) {
      spans.add(TextSpan(text: line, style: TextStyle(color: cCmt, fontStyle: FontStyle.italic)));
      if (li < lines.length - 1) spans.add(const TextSpan(text: '\n'));
      continue;
    }

    while (i < line.length) {
      final ch = line[i];

      // Inline comment
      if (i + 1 < line.length && ch == '-' && line[i+1] == '-') {
        spans.add(TextSpan(
            text: line.substring(i),
            style: TextStyle(color: cCmt, fontStyle: FontStyle.italic)));
        i = line.length;
        break;
      }

      // String
      if (ch == '"') {
        int j = i + 1;
        while (j < line.length && line[j] != '"') j++;
        spans.add(TextSpan(
            text: line.substring(i, j < line.length ? j + 1 : j),
            style: TextStyle(color: cStr)));
        i = j < line.length ? j + 1 : j;
        continue;
      }

      // Pipeline |
      if (ch == '|') {
        spans.add(TextSpan(text: '|', style: TextStyle(color: cPipe, fontWeight: FontWeight.bold)));
        i++;
        continue;
      }

      // Arrow ->
      if (ch == '-' && i + 1 < line.length && line[i+1] == '>') {
        spans.add(TextSpan(text: '->', style: TextStyle(color: cOp)));
        i += 2;
        continue;
      }

      // Number
      if (RegExp(r'\d').hasMatch(ch)) {
        int j = i;
        while (j < line.length && RegExp(r'[\d.]').hasMatch(line[j])) j++;
        spans.add(TextSpan(text: line.substring(i, j), style: TextStyle(color: cNum)));
        i = j;
        continue;
      }

      // Word
      if (RegExp(r'[a-zA-Z_]').hasMatch(ch)) {
        int j = i;
        while (j < line.length && RegExp(r'[a-zA-Z0-9_]').hasMatch(line[j])) j++;
        final word = line.substring(i, j);
        final isKw = keywords.contains(word);
        final isFunc = j < line.length && line[j] == '(';
        spans.add(TextSpan(
            text: word,
            style: TextStyle(
                color: isKw ? cKw : isFunc ? cFn : cDef,
                fontWeight: isKw ? FontWeight.bold : FontWeight.normal)));
        i = j;
        continue;
      }

      // Operators
      if ('=<>!+-*/%'.contains(ch)) {
        spans.add(TextSpan(text: ch, style: TextStyle(color: cOp)));
        i++;
        continue;
      }

      spans.add(TextSpan(text: ch, style: TextStyle(color: cDef)));
      i++;
    }

    if (li < lines.length - 1) spans.add(const TextSpan(text: '\n'));
  }
  return spans;
}

// ══════════════════════════════════════════════════════════════
// App Root
// ══════════════════════════════════════════════════════════════
class CreamIDEApp extends StatefulWidget {
  const CreamIDEApp({super.key});
  @override
  State<CreamIDEApp> createState() => _CreamIDEAppState();
}

class _CreamIDEAppState extends State<CreamIDEApp> {
  bool _isDark = true;
  String _langKey = 'English';
  String _projectFolder = '/storage/emulated/0/CreamProjects';

  String tr(String key) => kLang[_langKey]?[key] ?? key;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cream IDE',
      debugShowCheckedModeBanner: false,
      theme: _isDark ? _darkTheme() : _lightTheme(),
      home: IDEScreen(
        isDark: _isDark,
        langKey: _langKey,
        projectFolder: _projectFolder,
        onToggleTheme: () => setState(() => _isDark = !_isDark),
        onChangeLang: (l) => setState(() => _langKey = l),
        onChangeFolder: (f) => setState(() => _projectFolder = f),
        tr: tr,
      ),
    );
  }

  ThemeData _darkTheme() => ThemeData(
    brightness: Brightness.dark,
    scaffoldBackgroundColor: const Color(0xFF080b0f),
    colorScheme: const ColorScheme.dark(
        primary: Color(0xFF00ffe0), surface: Color(0xFF0d1117)),
    fontFamily: 'monospace',
    snackBarTheme: const SnackBarThemeData(behavior: SnackBarBehavior.floating),
  );

  ThemeData _lightTheme() => ThemeData(
    brightness: Brightness.light,
    scaffoldBackgroundColor: const Color(0xFFf6f8fa),
    colorScheme: const ColorScheme.light(
        primary: Color(0xFF0550ae), surface: Color(0xFFffffff)),
    fontFamily: 'monospace',
    snackBarTheme: const SnackBarThemeData(behavior: SnackBarBehavior.floating),
  );
}

// ══════════════════════════════════════════════════════════════
// IDE Screen
// ══════════════════════════════════════════════════════════════
class IDEScreen extends StatefulWidget {
  final bool isDark;
  final String langKey;
  final String projectFolder;
  final VoidCallback onToggleTheme;
  final Function(String) onChangeLang;
  final Function(String) onChangeFolder;
  final String Function(String) tr;

  const IDEScreen({
    super.key,
    required this.isDark,
    required this.langKey,
    required this.projectFolder,
    required this.onToggleTheme,
    required this.onChangeLang,
    required this.onChangeFolder,
    required this.tr,
  });

  @override
  State<IDEScreen> createState() => _IDEScreenState();
}

class _IDEScreenState extends State<IDEScreen> {
  String _currentFile = 'hello.cream';
  final Map<String, String> _files = Map.from(kSampleFiles);
  late TextEditingController _ctrl;
  final _outputScroll = ScrollController();
  final _editorScroll = ScrollController();
  final List<_OutputLine> _output = [];
  bool _drawerOpen = false;
  bool _outputOpen = false;
  bool _running = false;
  bool _highlight = true;

  // Theme helpers
  Color get bg     => widget.isDark ? const Color(0xFF080b0f) : const Color(0xFFf6f8fa);
  Color get bg2    => widget.isDark ? const Color(0xFF0d1117) : const Color(0xFFffffff);
  Color get bg3    => widget.isDark ? const Color(0xFF111820) : const Color(0xFFf0f4f8);
  Color get border => widget.isDark ? const Color(0xFF1e2d3d) : const Color(0xFFd0d7de);
  Color get accent => widget.isDark ? const Color(0xFF00ffe0) : const Color(0xFF0550ae);
  Color get acc2   => const Color(0xFFff6b9d);
  Color get dim    => widget.isDark ? const Color(0xFF546878) : const Color(0xFF6e7781);
  Color get txt    => widget.isDark ? const Color(0xFFc9d4e0) : const Color(0xFF24292e);

  @override
  void initState() {
    super.initState();
    _ctrl = TextEditingController(text: _files[_currentFile]);
    _ctrl.addListener(() {
      _files[_currentFile] = _ctrl.text;
      if (_highlight) setState(() {});
    });
  }

  @override
  void dispose() {
    _ctrl.dispose();
    _outputScroll.dispose();
    _editorScroll.dispose();
    super.dispose();
  }

  void _switchFile(String name) {
    _files[_currentFile] = _ctrl.text;
    setState(() {
      _currentFile = name;
      _ctrl.text = _files[name] ?? '';
      _drawerOpen = false;
    });
  }

  void _newFile() {
    final name = 'new_${_files.length}.cream';
    _files[name] = '-- New Cream file\n';
    _switchFile(name);
  }

  void _save() {
    _files[_currentFile] = _ctrl.text;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text('${widget.tr('save')}: $_currentFile',
          style: TextStyle(color: bg, fontFamily: 'monospace', fontSize: 12)),
      backgroundColor: accent,
      duration: const Duration(seconds: 2),
    ));
  }

  Future<void> _run() async {
    setState(() {
      _running = true;
      _output.clear();
      _output.add(_OutputLine('▶  ${widget.tr('running')} $_currentFile', _OType.info));
      _outputOpen = true;
    });

    await Future.delayed(const Duration(milliseconds: 500));

    // Mini Cream interpreter — handles variables, say, repeat, if, for each
    final lines = _ctrl.text.split('\n');
    bool hasOutput = false;
    final Map<String, dynamic> vars = {};

    // Helper: resolve a value (variable or literal)
    dynamic resolveVal(String raw) {
      raw = raw.trim();
      // String literal
      if (raw.startsWith('"') && raw.endsWith('"')) {
        return raw.substring(1, raw.length - 1);
      }
      // Boolean
      if (raw == 'yes') return true;
      if (raw == 'no') return false;
      if (raw == 'null') return null;
      // Number
      final n = num.tryParse(raw);
      if (n != null) return n;
      // Variable
      if (vars.containsKey(raw)) return vars[raw];
      return raw;
    }

    // Helper: interpolate {var} in string
    String interpolate(String s) {
      return s.replaceAllMapped(RegExp(r'\{([^}]+)\}'), (m) {
        final key = m.group(1)!.trim();
        final val = vars[key];
        if (val == null) return '{$key}';
        if (val is double && val == val.truncateToDouble()) {
          return val.toInt().toString();
        }
        return val.toString();
      });
    }

    // Helper: evaluate simple math expression
    dynamic evalExpr(String expr) {
      expr = expr.trim();
      // Simple binary ops
      for (final op in ['==', '!=', '>=', '<=', '>', '<', '+', '-', '*', '/', '%']) {
        final parts = expr.split(op);
        if (parts.length == 2) {
          final l = resolveVal(parts[0].trim());
          final r = resolveVal(parts[1].trim());
          try {
            switch (op) {
              case '+': return (l is num && r is num) ? l + r : '$l$r';
              case '-': return (l as num) - (r as num);
              case '*': return (l as num) * (r as num);
              case '/': return (l as num) / (r as num);
              case '%': return (l as num) % (r as num);
              case '==': return l == r;
              case '!=': return l != r;
              case '>':  return (l as num) > (r as num);
              case '<':  return (l as num) < (r as num);
              case '>=': return (l as num) >= (r as num);
              case '<=': return (l as num) <= (r as num);
            }
          } catch (_) {}
        }
      }
      return resolveVal(expr);
    }

    int i = 0;
    while (i < lines.length) {
      final raw = lines[i];
      final t = raw.trim();
      if (t.isEmpty || t.startsWith('--')) { i++; continue; }

      // Variable assignment: name = "value"
      final assignMatch = RegExp(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$').firstMatch(t);
      if (assignMatch != null && !t.startsWith('say') && !t.startsWith('if') &&
          !t.startsWith('for') && !t.startsWith('repeat') && !t.startsWith('action')) {
        final varName = assignMatch.group(1)!;
        final rawVal = assignMatch.group(2)!.trim();
        if (rawVal.startsWith('"') && rawVal.endsWith('"')) {
          vars[varName] = rawVal.substring(1, rawVal.length - 1);
        } else {
          vars[varName] = evalExpr(rawVal);
        }
        i++; continue;
      }

      // say
      if (t.startsWith('say ')) {
        var v = t.substring(4).trim();
        if (v.startsWith('"') && v.endsWith('"')) {
          v = v.substring(1, v.length - 1);
          v = interpolate(v);
        } else {
          final val = resolveVal(v);
          if (val is double && val == val.truncateToDouble()) {
            v = val.toInt().toString();
          } else {
            v = val?.toString() ?? 'null';
          }
        }
        _output.add(_OutputLine(v, _OType.normal));
        hasOutput = true;
        i++; continue;
      }

      // repeat N
      final repeatMatch = RegExp(r'^repeat\s+(\S+)').firstMatch(t);
      if (repeatMatch != null) {
        final count = (evalExpr(repeatMatch.group(1)!) as num).toInt();
        final body = <String>[];
        i++;
        while (i < lines.length && (lines[i].startsWith('    ') || lines[i].startsWith('\t'))) {
          body.add(lines[i].trim());
          i++;
        }
        for (int rep = 0; rep < count; rep++) {
          for (final bl in body) {
            if (bl.startsWith('say ')) {
              var v = bl.substring(4).trim();
              if (v.startsWith('"') && v.endsWith('"')) {
                v = interpolate(v.substring(1, v.length - 1));
              } else {
                v = resolveVal(v)?.toString() ?? 'null';
              }
              _output.add(_OutputLine(v, _OType.normal));
              hasOutput = true;
            }
          }
        }
        continue;
      }

      // for each x in [list] or range(...)
      final forMatch = RegExp(r'^for each (\w+) in (.+)$').firstMatch(t);
      if (forMatch != null) {
        final varN = forMatch.group(1)!;
        final iterStr = forMatch.group(2)!.trim();
        List<dynamic> items = [];
        final rangeMatch = RegExp(r'^range\((\d+),\s*(\d+)(?:,\s*(\d+))?\)$').firstMatch(iterStr);
        if (rangeMatch != null) {
          final from = int.parse(rangeMatch.group(1)!);
          final to   = int.parse(rangeMatch.group(2)!);
          final step = rangeMatch.group(3) != null ? int.parse(rangeMatch.group(3)!) : 1;
          for (int n = from; n < to; n += step) items.add(n);
        }
        final body = <String>[];
        i++;
        while (i < lines.length && (lines[i].startsWith('    ') || lines[i].startsWith('\t'))) {
          body.add(lines[i].trim());
          i++;
        }
        for (final item in items) {
          vars[varN] = item;
          for (final bl in body) {
            if (bl.startsWith('say ')) {
              var v = bl.substring(4).trim();
              if (v.startsWith('"') && v.endsWith('"')) {
                v = interpolate(v.substring(1, v.length - 1));
              } else {
                final val = resolveVal(v);
                if (val is double && val == val.truncateToDouble()) {
                  v = val.toInt().toString();
                } else {
                  v = val?.toString() ?? 'null';
                }
              }
              _output.add(_OutputLine(v, _OType.normal));
              hasOutput = true;
            }
          }
        }
        continue;
      }

      i++;
    }

    if (!hasOutput) {
      _output.add(_OutputLine(
          'Note: connect real cream.py for full execution.',
          _OType.warn));
    }

    _output.add(_OutputLine('', _OType.normal));
    _output.add(_OutputLine('✓  ${widget.tr('done')}', _OType.success));

    setState(() => _running = false);

    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_outputScroll.hasClients) {
        _outputScroll.animateTo(
          _outputScroll.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final pad = MediaQuery.of(context).padding;
    return Scaffold(
      backgroundColor: bg,
      body: Stack(children: [
        Column(children: [
          SizedBox(height: pad.top),
          _topBar(),
          Expanded(child: _outputOpen
              ? Column(children: [
            Expanded(flex: 6, child: _editor()),
            _outputDivider(),
            SizedBox(height: 220, child: _outputPanel()),
          ])
              : _editor()),
        ]),
        if (_drawerOpen) ...[
          GestureDetector(
            onTap: () => setState(() => _drawerOpen = false),
            child: Container(color: Colors.black54),
          ),
          _drawer(pad),
        ],
      ]),
      bottomNavigationBar: _bottomBar(pad),
    );
  }

  // ── Top bar ──
  Widget _topBar() => Container(
    height: 52,
    decoration: BoxDecoration(color: bg2, border: Border(bottom: BorderSide(color: border))),
    child: Row(children: [
      _iBtn(Icons.menu, () => setState(() => _drawerOpen = !_drawerOpen)),
      Padding(
        padding: const EdgeInsets.symmetric(horizontal: 4),
        child: RichText(text: TextSpan(children: [
          TextSpan(text: '[', style: TextStyle(color: accent, fontSize: 14, fontWeight: FontWeight.bold)),
          TextSpan(text: 'cream', style: TextStyle(color: widget.isDark ? Colors.white : const Color(0xFF1f2328), fontSize: 14, fontWeight: FontWeight.bold)),
          TextSpan(text: ']', style: TextStyle(color: accent, fontSize: 14, fontWeight: FontWeight.bold)),
        ])),
      ),
      Expanded(
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 9, horizontal: 2),
          padding: const EdgeInsets.symmetric(horizontal: 8),
          decoration: BoxDecoration(color: bg3, border: Border.all(color: border)),
          child: Row(children: [
            Icon(Icons.insert_drive_file_outlined, size: 11, color: dim),
            const SizedBox(width: 5),
            Expanded(child: Text(_currentFile, overflow: TextOverflow.ellipsis,
                style: TextStyle(color: txt, fontSize: 11))),
          ]),
        ),
      ),
      _iBtn(Icons.settings_outlined, _showSettings),
      const SizedBox(width: 4),
    ]),
  );

  // ── Editor ──
  Widget _editor() => Row(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      // Line numbers
      Container(
        width: 38, color: bg2,
        padding: const EdgeInsets.only(top: 10, right: 6),
        child: SingleChildScrollView(
          controller: _editorScroll,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: List.generate(
              _ctrl.text.split('\n').length,
                  (i) => Text('${i+1}', style: TextStyle(
                  color: dim, fontSize: 11, height: 1.55, fontFamily: 'monospace')),
            ),
          ),
        ),
      ),
      Container(width: 1, color: border),
      // Code
      Expanded(child: _highlight ? _richEditor() : _plainEditor()),
    ],
  );

  Widget _richEditor() => Stack(children: [
    TextField(
      controller: _ctrl, maxLines: null, expands: true,
      style: const TextStyle(color: Colors.transparent, fontSize: 13, height: 1.55, fontFamily: 'monospace'),
      decoration: const InputDecoration(border: InputBorder.none, contentPadding: EdgeInsets.all(10)),
      cursorColor: accent,
      keyboardType: TextInputType.multiline,
      textInputAction: TextInputAction.newline,
    ),
    IgnorePointer(
      child: Padding(
        padding: const EdgeInsets.all(10),
        child: RichText(text: TextSpan(
          children: highlightCream(_ctrl.text, widget.isDark),
          style: const TextStyle(fontSize: 13, height: 1.55, fontFamily: 'monospace'),
        )),
      ),
    ),
  ]);

  Widget _plainEditor() => TextField(
    controller: _ctrl, maxLines: null, expands: true,
    style: TextStyle(color: txt, fontSize: 13, height: 1.55, fontFamily: 'monospace'),
    decoration: const InputDecoration(border: InputBorder.none, contentPadding: EdgeInsets.all(10)),
    cursorColor: accent,
    keyboardType: TextInputType.multiline,
    textInputAction: TextInputAction.newline,
  );

  // ── Output divider ──
  Widget _outputDivider() => Container(
    height: 32, color: bg2,
    padding: const EdgeInsets.symmetric(horizontal: 12),
    decoration: BoxDecoration(border: Border(top: BorderSide(color: border), bottom: BorderSide(color: border))),
    child: Row(children: [
      Icon(Icons.terminal, size: 13, color: accent),
      const SizedBox(width: 6),
      Text(widget.tr('output').toUpperCase(),
          style: TextStyle(color: accent, fontSize: 10, letterSpacing: 2)),
      const Spacer(),
      GestureDetector(
        onTap: () => setState(() => _output.clear()),
        child: Text(widget.tr('clear'), style: TextStyle(color: dim, fontSize: 11)),
      ),
      const SizedBox(width: 14),
      GestureDetector(
        onTap: () => setState(() => _outputOpen = false),
        child: Icon(Icons.close, size: 15, color: dim),
      ),
    ]),
  );

  // ── Output panel ──
  Widget _outputPanel() => Container(
    color: bg2,
    child: _output.isEmpty
        ? Center(child: Text(widget.tr('nooutput'),
        style: TextStyle(color: dim, fontSize: 12)))
        : ListView.builder(
        controller: _outputScroll,
        padding: const EdgeInsets.all(10),
        itemCount: _output.length,
        itemBuilder: (_, i) {
          final o = _output[i];
          return Text(o.text, style: TextStyle(
              color: o.color(accent, widget.isDark),
              fontSize: 12, fontFamily: 'monospace', height: 1.6));
        }),
  );

  // ── Bottom bar ──
  Widget _bottomBar(EdgeInsets pad) => Container(
    height: 52 + pad.bottom,
    padding: EdgeInsets.only(bottom: pad.bottom),
    decoration: BoxDecoration(color: bg2, border: Border(top: BorderSide(color: border))),
    child: Row(children: [
      const SizedBox(width: 8),
      // Run
      Expanded(flex: 3, child: GestureDetector(
        onTap: _running ? null : _run,
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 4),
          color: _running ? border : accent,
          child: Center(child: _running
              ? SizedBox(width: 16, height: 16,
              child: CircularProgressIndicator(strokeWidth: 2, color: bg))
              : Row(mainAxisSize: MainAxisSize.min, children: [
            Icon(Icons.play_arrow, size: 16, color: bg),
            const SizedBox(width: 4),
            Text(widget.tr('run'),
                style: TextStyle(color: bg, fontWeight: FontWeight.bold, fontSize: 13)),
          ])),
        ),
      )),
      // Output toggle
      Expanded(flex: 2, child: GestureDetector(
        onTap: () => setState(() => _outputOpen = !_outputOpen),
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 4),
          decoration: BoxDecoration(
            color: _outputOpen ? accent.withOpacity(0.12) : bg3,
            border: Border.all(color: _outputOpen ? accent : border),
          ),
          child: Center(child: Row(mainAxisSize: MainAxisSize.min, children: [
            Icon(Icons.terminal, size: 14, color: _outputOpen ? accent : dim),
            const SizedBox(width: 4),
            Text(widget.tr('output'),
                style: TextStyle(color: _outputOpen ? accent : dim, fontSize: 12)),
          ])),
        ),
      )),
      _iBtn(Icons.save_outlined, _save),
      _iBtn(widget.isDark ? Icons.light_mode_outlined : Icons.dark_mode_outlined,
          widget.onToggleTheme),
      const SizedBox(width: 4),
    ]),
  );

  // ── File Drawer ──
  Widget _drawer(EdgeInsets pad) => Positioned(
    top: 0, left: 0, bottom: 0, width: 255,
    child: Container(
      padding: EdgeInsets.only(top: pad.top),
      decoration: BoxDecoration(color: bg2, border: Border(right: BorderSide(color: border))),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        // Header
        Container(
          height: 52,
          padding: const EdgeInsets.symmetric(horizontal: 14),
          decoration: BoxDecoration(border: Border(bottom: BorderSide(color: border))),
          child: Row(children: [
            Icon(Icons.folder_outlined, size: 14, color: accent),
            const SizedBox(width: 8),
            Text(widget.tr('files').toUpperCase(),
                style: TextStyle(color: accent, fontSize: 10, letterSpacing: 2)),
            const Spacer(),
            GestureDetector(onTap: _newFile, child: Icon(Icons.add, size: 18, color: dim)),
          ]),
        ),
        // Folder path
        Padding(
          padding: const EdgeInsets.fromLTRB(14, 6, 14, 4),
          child: Text(widget.projectFolder,
              style: TextStyle(color: dim, fontSize: 9), overflow: TextOverflow.ellipsis),
        ),
        Container(height: 1, color: border),
        // File list
        Expanded(
          child: ListView(
            children: _files.keys.map((name) {
              final active = name == _currentFile;
              return GestureDetector(
                onTap: () => _switchFile(name),
                child: Container(
                  color: active ? accent.withOpacity(0.08) : Colors.transparent,
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                  child: Row(children: [
                    Container(width: 2, height: 14, color: active ? accent : Colors.transparent),
                    const SizedBox(width: 8),
                    Icon(Icons.insert_drive_file_outlined, size: 13, color: active ? accent : dim),
                    const SizedBox(width: 8),
                    Expanded(child: Text(name, overflow: TextOverflow.ellipsis,
                        style: TextStyle(color: active ? accent : txt, fontSize: 13))),
                  ]),
                ),
              );
            }).toList(),
          ),
        ),
        Container(height: 1, color: border),
        GestureDetector(
          onTap: _newFile,
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Row(children: [
              Icon(Icons.add, size: 14, color: accent),
              const SizedBox(width: 8),
              Text(widget.tr('newfile'), style: TextStyle(color: accent, fontSize: 13)),
            ]),
          ),
        ),
      ]),
    ),
  );

  // ── Settings ──
  void _showSettings() {
    final folderCtrl = TextEditingController(text: widget.projectFolder);
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: bg2,
      shape: const RoundedRectangleBorder(),
      builder: (_) => StatefulBuilder(
        builder: (ctx, setS) => DraggableScrollableSheet(
          expand: false,
          initialChildSize: 0.8,
          builder: (_, sc) => Column(children: [
            Container(
              margin: const EdgeInsets.only(top: 10, bottom: 6),
              width: 40, height: 4,
              decoration: BoxDecoration(color: border, borderRadius: BorderRadius.circular(2)),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
              child: Row(children: [
                Text(widget.tr('settings').toUpperCase(),
                    style: TextStyle(color: accent, fontSize: 11, letterSpacing: 2)),
              ]),
            ),
            Container(height: 1, color: border),
            Expanded(
              child: ListView(controller: sc, padding: const EdgeInsets.all(16), children: [

                // Theme
                _sLabel(widget.tr('theme')),
                Row(children: [
                  _tBtn(widget.tr('dark'), true, setS),
                  const SizedBox(width: 8),
                  _tBtn(widget.tr('light'), false, setS),
                ]),
                const SizedBox(height: 20),

                // Language
                _sLabel(widget.tr('language')),
                Wrap(spacing: 6, runSpacing: 6,
                  children: kLang.keys.map((l) {
                    final sel = l == widget.langKey;
                    return GestureDetector(
                      onTap: () { widget.onChangeLang(l); Navigator.pop(context); },
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                        decoration: BoxDecoration(
                          color: sel ? accent.withOpacity(0.12) : bg3,
                          border: Border.all(color: sel ? accent : border),
                        ),
                        child: Text(l, style: TextStyle(color: sel ? accent : txt, fontSize: 12)),
                      ),
                    );
                  }).toList(),
                ),
                const SizedBox(height: 20),

                // Project folder
                _sLabel(widget.tr('folder')),
                Container(
                  decoration: BoxDecoration(color: bg3, border: Border.all(color: border)),
                  padding: const EdgeInsets.symmetric(horizontal: 10),
                  child: TextField(
                    controller: folderCtrl,
                    style: TextStyle(color: txt, fontSize: 12, fontFamily: 'monospace'),
                    decoration: InputDecoration(
                      border: InputBorder.none,
                      hintText: '/storage/emulated/0/CreamProjects',
                      hintStyle: TextStyle(color: dim, fontSize: 12),
                    ),
                  ),
                ),
                const SizedBox(height: 8),
                GestureDetector(
                  onTap: () { widget.onChangeFolder(folderCtrl.text); Navigator.pop(context); },
                  child: Container(
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    color: accent,
                    child: Center(child: Text(widget.tr('save'),
                        style: TextStyle(color: bg, fontWeight: FontWeight.bold))),
                  ),
                ),
                const SizedBox(height: 20),

                // Syntax highlight
                _sLabel(widget.tr('highlight')),
                Row(children: [
                  Switch(value: _highlight, activeColor: accent,
                      onChanged: (v) { setState(() => _highlight = v); setS(() {}); }),
                  Text(_highlight ? 'ON' : 'OFF',
                      style: TextStyle(color: txt, fontSize: 13)),
                ]),
                const SizedBox(height: 8),
              ]),
            ),
          ]),
        ),
      ),
    );
  }

  Widget _sLabel(String l) => Padding(
    padding: const EdgeInsets.only(bottom: 8),
    child: Text(l.toUpperCase(), style: TextStyle(color: dim, fontSize: 9, letterSpacing: 1.5)),
  );

  Widget _tBtn(String label, bool dark, StateSetter setS) {
    final sel = widget.isDark == dark;
    return GestureDetector(
      onTap: sel ? null : () { widget.onToggleTheme(); setS(() {}); setState(() {}); },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: sel ? accent.withOpacity(0.12) : bg3,
          border: Border.all(color: sel ? accent : border),
        ),
        child: Text(label, style: TextStyle(color: sel ? accent : txt, fontSize: 13)),
      ),
    );
  }

  Widget _iBtn(IconData icon, VoidCallback onTap) => InkWell(
    onTap: onTap,
    child: SizedBox(width: 44, height: 52, child: Icon(icon, color: dim, size: 20)),
  );
}

// ── Output line types ──
enum _OType { normal, info, success, warn, error }

class _OutputLine {
  final String text;
  final _OType type;
  const _OutputLine(this.text, this.type);

  Color color(Color accent, bool isDark) {
    switch (type) {
      case _OType.info:    return accent;
      case _OType.success: return const Color(0xFFa8ff78);
      case _OType.warn:    return const Color(0xFFffab70);
      case _OType.error:   return Colors.redAccent;
      case _OType.normal:  return isDark ? const Color(0xFFc9d4e0) : const Color(0xFF24292e);
    }
  }
}