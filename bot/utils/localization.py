"""UI string localization for multi-language support"""

from typing import Dict, Optional

# Category translations (English -> localized)
# These are ACNH item categories stored in the database
CATEGORY_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'ja': {
        'Accessories': 'アクセサリー',
        'Art': 'びじゅつひん',
        'Bags': 'バッグ',
        'Bottoms': 'ボトムス',
        'Bugs': 'ムシ',
        'Clothing Other': 'そのほかのふく',
        'Dress-Up': 'ワンピース',
        'Fencing': 'さく',
        'Fish': 'さかな',
        'Floors': 'ゆか',
        'Fossils': 'かせき',
        'Gyroids': 'はにわ',
        'Headwear': 'ぼうし',
        'Housewares': 'かぐ',
        'Miscellaneous': 'こもの',
        'Music': 'ミュージック',
        'Photos': 'しゃしん',
        'Posters': 'ポスター',
        'Recipes': 'レシピ',
        'Rugs': 'ラグ',
        'Sea Creatures': 'うみのさち',
        'Shoes': 'くつ',
        'Socks': 'くつした',
        'Tools': 'どうぐ',
        'Tops': 'トップス',
        'Umbrellas': 'かさ',
        'Wall-mounted': 'かべかけ',
        'Wallpaper': 'かべがみ',
    },
    'zh': {
        'Accessories': '配饰',
        'Art': '艺术品',
        'Bags': '包包',
        'Bottoms': '下装',
        'Bugs': '虫类',
        'Clothing Other': '其他服装',
        'Dress-Up': '连衣裙',
        'Fencing': '栅栏',
        'Fish': '鱼类',
        'Floors': '地板',
        'Fossils': '化石',
        'Gyroids': '土偶',
        'Headwear': '帽子',
        'Housewares': '家具',
        'Miscellaneous': '杂货',
        'Music': '音乐',
        'Photos': '照片',
        'Posters': '海报',
        'Recipes': '食谱',
        'Rugs': '地毯',
        'Sea Creatures': '海洋生物',
        'Shoes': '鞋子',
        'Socks': '袜子',
        'Tools': '工具',
        'Tops': '上衣',
        'Umbrellas': '雨伞',
        'Wall-mounted': '壁挂',
        'Wallpaper': '壁纸',
    },
    'ko': {
        'Accessories': '액세서리',
        'Art': '미술품',
        'Bags': '가방',
        'Bottoms': '하의',
        'Bugs': '곤충',
        'Clothing Other': '기타 의류',
        'Dress-Up': '원피스',
        'Fencing': '울타리',
        'Fish': '물고기',
        'Floors': '바닥',
        'Fossils': '화석',
        'Gyroids': '토용',
        'Headwear': '모자',
        'Housewares': '가구',
        'Miscellaneous': '잡화',
        'Music': '음악',
        'Photos': '사진',
        'Posters': '포스터',
        'Recipes': '레시피',
        'Rugs': '러그',
        'Sea Creatures': '해산물',
        'Shoes': '신발',
        'Socks': '양말',
        'Tools': '도구',
        'Tops': '상의',
        'Umbrellas': '우산',
        'Wall-mounted': '벽걸이',
        'Wallpaper': '벽지',
    },
    'fr': {
        'Accessories': 'Accessoires',
        'Art': 'Œuvres d\'art',
        'Bags': 'Sacs',
        'Bottoms': 'Bas',
        'Bugs': 'Insectes',
        'Clothing Other': 'Autres vêtements',
        'Dress-Up': 'Robes',
        'Fencing': 'Clôtures',
        'Fish': 'Poissons',
        'Floors': 'Sols',
        'Fossils': 'Fossiles',
        'Gyroids': 'Gyroïdes',
        'Headwear': 'Chapeaux',
        'Housewares': 'Mobilier',
        'Miscellaneous': 'Divers',
        'Music': 'Musique',
        'Photos': 'Photos',
        'Posters': 'Posters',
        'Recipes': 'Recettes',
        'Rugs': 'Tapis',
        'Sea Creatures': 'Créatures marines',
        'Shoes': 'Chaussures',
        'Socks': 'Chaussettes',
        'Tools': 'Outils',
        'Tops': 'Hauts',
        'Umbrellas': 'Parapluies',
        'Wall-mounted': 'Objets muraux',
        'Wallpaper': 'Papiers peints',
    },
    'de': {
        'Accessories': 'Accessoires',
        'Art': 'Kunstwerke',
        'Bags': 'Taschen',
        'Bottoms': 'Unterteile',
        'Bugs': 'Insekten',
        'Clothing Other': 'Sonstige Kleidung',
        'Dress-Up': 'Kleider',
        'Fencing': 'Zäune',
        'Fish': 'Fische',
        'Floors': 'Böden',
        'Fossils': 'Fossilien',
        'Gyroids': 'Gyroiden',
        'Headwear': 'Kopfbedeckungen',
        'Housewares': 'Möbel',
        'Miscellaneous': 'Verschiedenes',
        'Music': 'Musik',
        'Photos': 'Fotos',
        'Posters': 'Poster',
        'Recipes': 'Rezepte',
        'Rugs': 'Teppiche',
        'Sea Creatures': 'Meerestiere',
        'Shoes': 'Schuhe',
        'Socks': 'Socken',
        'Tools': 'Werkzeuge',
        'Tops': 'Oberteile',
        'Umbrellas': 'Regenschirme',
        'Wall-mounted': 'Wandobjekte',
        'Wallpaper': 'Tapeten',
    },
    'es': {
        'Accessories': 'Accesorios',
        'Art': 'Obras de arte',
        'Bags': 'Bolsos',
        'Bottoms': 'Partes inferiores',
        'Bugs': 'Insectos',
        'Clothing Other': 'Otra ropa',
        'Dress-Up': 'Vestidos',
        'Fencing': 'Vallas',
        'Fish': 'Peces',
        'Floors': 'Suelos',
        'Fossils': 'Fósiles',
        'Gyroids': 'Gyroiditas',
        'Headwear': 'Sombreros',
        'Housewares': 'Muebles',
        'Miscellaneous': 'Varios',
        'Music': 'Música',
        'Photos': 'Fotos',
        'Posters': 'Pósteres',
        'Recipes': 'Recetas',
        'Rugs': 'Alfombras',
        'Sea Creatures': 'Criaturas marinas',
        'Shoes': 'Zapatos',
        'Socks': 'Calcetines',
        'Tools': 'Herramientas',
        'Tops': 'Partes superiores',
        'Umbrellas': 'Paraguas',
        'Wall-mounted': 'Objetos de pared',
        'Wallpaper': 'Papel pintado',
    },
    'it': {
        'Accessories': 'Accessori',
        'Art': 'Opere d\'arte',
        'Bags': 'Borse',
        'Bottoms': 'Pantaloni',
        'Bugs': 'Insetti',
        'Clothing Other': 'Altri vestiti',
        'Dress-Up': 'Abiti',
        'Fencing': 'Recinzioni',
        'Fish': 'Pesci',
        'Floors': 'Pavimenti',
        'Fossils': 'Fossili',
        'Gyroids': 'Giroidi',
        'Headwear': 'Cappelli',
        'Housewares': 'Mobili',
        'Miscellaneous': 'Varie',
        'Music': 'Musica',
        'Photos': 'Foto',
        'Posters': 'Poster',
        'Recipes': 'Ricette',
        'Rugs': 'Tappeti',
        'Sea Creatures': 'Creature marine',
        'Shoes': 'Scarpe',
        'Socks': 'Calzini',
        'Tools': 'Attrezzi',
        'Tops': 'Magliette',
        'Umbrellas': 'Ombrelli',
        'Wall-mounted': 'Oggetti da parete',
        'Wallpaper': 'Carta da parati',
    },
    'nl': {
        'Accessories': 'Accessoires',
        'Art': 'Kunst',
        'Bags': 'Tassen',
        'Bottoms': 'Onderkleding',
        'Bugs': 'Insecten',
        'Clothing Other': 'Overige kleding',
        'Dress-Up': 'Jurken',
        'Fencing': 'Hekken',
        'Fish': 'Vissen',
        'Floors': 'Vloeren',
        'Fossils': 'Fossielen',
        'Gyroids': 'Gyroïden',
        'Headwear': 'Hoofddeksels',
        'Housewares': 'Meubels',
        'Miscellaneous': 'Diversen',
        'Music': 'Muziek',
        'Photos': 'Foto\'s',
        'Posters': 'Posters',
        'Recipes': 'Recepten',
        'Rugs': 'Tapijten',
        'Sea Creatures': 'Zeedieren',
        'Shoes': 'Schoenen',
        'Socks': 'Sokken',
        'Tools': 'Gereedschap',
        'Tops': 'Bovenkleding',
        'Umbrellas': 'Paraplu\'s',
        'Wall-mounted': 'Wandobjecten',
        'Wallpaper': 'Behang',
    },
    'ru': {
        'Accessories': 'Аксессуары',
        'Art': 'Искусство',
        'Bags': 'Сумки',
        'Bottoms': 'Низ',
        'Bugs': 'Насекомые',
        'Clothing Other': 'Другая одежда',
        'Dress-Up': 'Платья',
        'Fencing': 'Заборы',
        'Fish': 'Рыба',
        'Floors': 'Полы',
        'Fossils': 'Окаменелости',
        'Gyroids': 'Гироиды',
        'Headwear': 'Головные уборы',
        'Housewares': 'Мебель',
        'Miscellaneous': 'Разное',
        'Music': 'Музыка',
        'Photos': 'Фотографии',
        'Posters': 'Постеры',
        'Recipes': 'Рецепты',
        'Rugs': 'Ковры',
        'Sea Creatures': 'Морские существа',
        'Shoes': 'Обувь',
        'Socks': 'Носки',
        'Tools': 'Инструменты',
        'Tops': 'Верх',
        'Umbrellas': 'Зонты',
        'Wall-mounted': 'Настенные предметы',
        'Wallpaper': 'Обои',
    },
}

# Source translations (English -> localized)
# These are common ACNH item sources
SOURCE_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'ja': {
        'Crafting': 'DIY',
        'Nook Shopping': 'たぬきショッピング',
        'Nook\'s Cranny': 'たぬきち商店',
        'Able Sisters': 'エイブルシスターズ',
        'Resident Services': '案内所',
        'Fishing': 'つり',
        'Bug Catching': 'ムシとり',
        'Diving': 'そせん',
        'Balloon': 'ふうせん',
        'Message Bottle': 'メッセージボトル',
        'Villager': 'じゅうみん',
        'NPC': 'NPC',
        'Event': 'イベント',
        'Seasonal': 'きせつ',
        'Fossils': 'かせき',
        'Kicks': 'シャンク',
        'Label': 'ことの',
        'Redd': 'つねきち',
        'CJ': 'ジャスティン',
        'Flick': 'レックス',
        'Leif': 'レイジ',
        'Saharah': 'ローラン',
        'Celeste': 'フーコ',
        'Gullivarrr': 'かいぞく',
        'Gulliver': 'ジョニー',
        'Wisp': 'ゆうたろう',
        'Pascal': 'ラコスケ',
        'Mom': 'ははのて',
        'Birthday': 'たんじょうび',
        'Wedding': 'ジューンブライド',
        'Bug-Off': 'ムシとり大会',
        'Fishing Tourney': 'つり大会',
        'Treasure Island': 'りそうのじま',
        'Harvey\'s Island': 'パニーのしま',
        'Kapp\'n Tour': 'かっぺいツアー',
        'HHP': 'ハッピーホームパラダイス',
    },
    'zh': {
        'Crafting': 'DIY',
        'Nook Shopping': '狸端机',
        'Nook\'s Cranny': '狸猫商店',
        'Able Sisters': '服装店',
        'Resident Services': '服务处',
        'Fishing': '钓鱼',
        'Bug Catching': '捉虫',
        'Diving': '潜水',
        'Balloon': '气球',
        'Message Bottle': '漂流瓶',
        'Villager': '居民',
        'Event': '活动',
        'Seasonal': '季节',
    },
    'ko': {
        'Crafting': 'DIY',
        'Nook Shopping': '너굴 쇼핑',
        'Nook\'s Cranny': '너굴 상점',
        'Able Sisters': '에이블 시스터즈',
        'Resident Services': '안내소',
        'Fishing': '낚시',
        'Bug Catching': '곤충 채집',
        'Diving': '잠수',
        'Balloon': '풍선',
        'Message Bottle': '유리병 편지',
        'Villager': '주민',
        'Event': '이벤트',
        'Seasonal': '계절',
    },
    'fr': {
        'Crafting': 'Bricolage',
        'Nook Shopping': 'Nook Shopping',
        'Nook\'s Cranny': 'Boutique Nook',
        'Able Sisters': 'Boutique des sœurs Doigts de fée',
        'Resident Services': 'Bureau des résidents',
        'Fishing': 'Pêche',
        'Bug Catching': 'Chasse aux insectes',
        'Diving': 'Plongée',
        'Balloon': 'Ballon',
        'Message Bottle': 'Bouteille à la mer',
        'Villager': 'Habitant',
        'Event': 'Événement',
        'Seasonal': 'Saisonnier',
    },
    'de': {
        'Crafting': 'Heimwerken',
        'Nook Shopping': 'Nook Shopping',
        'Nook\'s Cranny': 'Nooks Laden',
        'Able Sisters': 'Schneiderei',
        'Resident Services': 'Servicecenter',
        'Fishing': 'Angeln',
        'Bug Catching': 'Insektenfang',
        'Diving': 'Tauchen',
        'Balloon': 'Ballon',
        'Message Bottle': 'Flaschenpost',
        'Villager': 'Bewohner',
        'Event': 'Event',
        'Seasonal': 'Saisonal',
    },
    'es': {
        'Crafting': 'Bricolaje',
        'Nook Shopping': 'Nook Shopping',
        'Nook\'s Cranny': 'Tienda Nook',
        'Able Sisters': 'Hermanas Manitas',
        'Resident Services': 'Oficina de Gestión',
        'Fishing': 'Pesca',
        'Bug Catching': 'Caza de bichos',
        'Diving': 'Buceo',
        'Balloon': 'Globo',
        'Message Bottle': 'Botella con mensaje',
        'Villager': 'Vecino',
        'Event': 'Evento',
        'Seasonal': 'Estacional',
    },
    'it': {
        'Crafting': 'Fai da te',
        'Nook Shopping': 'Nook Shopping',
        'Nook\'s Cranny': 'Bottega di Nook',
        'Able Sisters': 'Ago e Filo',
        'Resident Services': 'Ufficio Servizi',
        'Fishing': 'Pesca',
        'Bug Catching': 'Caccia agli insetti',
        'Diving': 'Immersione',
        'Balloon': 'Palloncino',
        'Message Bottle': 'Bottiglia con messaggio',
        'Villager': 'Abitante',
        'Event': 'Evento',
        'Seasonal': 'Stagionale',
    },
    'nl': {
        'Crafting': 'Knutselen',
        'Nook Shopping': 'Nook Shopping',
        'Nook\'s Cranny': 'Nooks Winkel',
        'Able Sisters': 'Able-zusters',
        'Resident Services': 'Servicebalie',
        'Fishing': 'Vissen',
        'Bug Catching': 'Insecten vangen',
        'Diving': 'Duiken',
        'Balloon': 'Ballon',
        'Message Bottle': 'Fles met bericht',
        'Villager': 'Bewoner',
        'Event': 'Evenement',
        'Seasonal': 'Seizoensgebonden',
    },
    'ru': {
        'Crafting': 'Крафт',
        'Nook Shopping': 'Нук Шоппинг',
        'Nook\'s Cranny': 'Лавка Нука',
        'Able Sisters': 'Сёстры Эйбл',
        'Resident Services': 'Ратуша',
        'Fishing': 'Рыбалка',
        'Bug Catching': 'Ловля насекомых',
        'Diving': 'Дайвинг',
        'Balloon': 'Шарик',
        'Message Bottle': 'Бутылка с посланием',
        'Villager': 'Житель',
        'Event': 'Событие',
        'Seasonal': 'Сезонный',
    },
}


def translate_category(category: str, language: str) -> str:
    """Translate a category name to the user's language.
    
    Args:
        category: English category name from database (may be any case)
        language: Target language code
    
    Returns:
        Translated category or original if no translation found
    """
    if language == 'en' or not category:
        return category
    
    lang_categories = CATEGORY_TRANSLATIONS.get(language, {})
    
    # Try exact match first
    if category in lang_categories:
        return lang_categories[category]
    
    # Try case-insensitive match (database may have lowercase)
    category_lower = category.lower()
    for eng_cat, translated in lang_categories.items():
        if eng_cat.lower() == category_lower:
            return translated
    
    return category


def translate_source(source: str, language: str) -> str:
    """Translate a source name to the user's language.
    
    Args:
        source: English source name from database (may be any case)
        language: Target language code
    
    Returns:
        Translated source or original if no translation found
    """
    if language == 'en' or not source:
        return source
    
    lang_sources = SOURCE_TRANSLATIONS.get(language, {})
    
    # Try exact match first
    if source in lang_sources:
        return lang_sources[source]
    
    # Try case-insensitive match
    source_lower = source.lower()
    for eng_src, translated in lang_sources.items():
        if eng_src.lower() == source_lower:
            return translated
    
    return source


# UI strings organized by language
# Each language has the same keys for consistency
UI_STRINGS: Dict[str, Dict[str, str]] = {
    'en': {
        # Embed labels
        'category': 'Category',
        'sell_price': 'Sell Price',
        'buy_price': 'Buy Price',
        'source': 'Source',
        'details': 'Details',
        'variant': 'Variant',
        'default': 'Default',
        'item_hex': 'Item Hex',
        'hex': 'Hex',
        'ti_customize': 'TI Customize',
        'hha_info': 'HHA Info',
        'hha_points': 'HHA Points',
        'customizable': 'Customizable',
        'bells': 'Bells',
        'variants': 'Variants',
        'variants_available': 'available',
        
        # Buttons
        'add_to_stash': 'Add to Stash',
        'refresh_images': 'Refresh Images',
        'nookipedia': 'Nookipedia',
        'cancel': 'Cancel',
        'confirm': 'Confirm',
        
        # Stash UI
        'stash': 'Stash',
        'item': 'Item',
        'quantity': 'Quantity',
        'items': 'items',
        'select_stash': 'Choose a stash...',
        'stash_full': 'Stash Full',
        'added_to_stash': 'Added to Stash',
        'partially_added': 'Partially Added',
        'error': 'Error',
        
        # Search/Results
        'no_results': 'No Results',
        'search_results': 'Search Results',
        'lookup_results': 'Lookup Results',
        
        # Footer messages
        'images_refreshed': 'Images refreshed',
        'buttons_expired': 'Buttons have expired - use the command again to interact',
        
        # Variation footer (use {count} as placeholder)
        'item_has': 'This item has',
        'variations': 'variations',
        'patterns': 'patterns',
        'and': 'and',
        
        # Variant selector
        'choose_variant': 'Choose a variant...',
        'choose_variant_page': 'Choose variant (Page {page}/{total})...',
        
        # Preference dialogs
        'language_updated': 'Language Updated',
        'language_set_to': 'Your preferred language is now',
        'what_this_means': 'What this means',
        'language_benefits': '• Item searches will match names in your language\n• Item details will show names in your language when available',
        'language_update_failed': 'Failed to update language preference. Please try again.',
        'language_set': 'Language Set!',
        'enjoy_nooklook': "You're all set! Enjoy using NookLook.",
        'change_anytime': 'Change anytime with /language',
    },
    'ja': {
        # Embed labels
        'category': 'カテゴリー',
        'sell_price': '売値',
        'buy_price': '買値',
        'source': '入手方法',
        'details': '詳細',
        'variant': 'バリエーション',
        'default': 'デフォルト',
        'item_hex': 'アイテムHex',
        'hex': 'Hex',
        'ti_customize': 'TIカスタマイズ',
        'hha_info': 'HHA情報',
        'hha_points': 'HHAポイント',
        'customizable': 'カスタマイズ可能',
        'bells': 'ベル',
        'variants': 'バリエーション',
        'variants_available': '利用可能',
        
        # Buttons
        'add_to_stash': 'スタッシュに追加',
        'refresh_images': '画像を更新',
        'nookipedia': 'Nookipedia',
        'cancel': 'キャンセル',
        'confirm': '確認',
        
        # Stash UI
        'stash': 'スタッシュ',
        'item': 'アイテム',
        'quantity': '数量',
        'items': 'アイテム',
        'select_stash': 'スタッシュを選択...',
        'stash_full': 'スタッシュがいっぱいです',
        'added_to_stash': 'スタッシュに追加しました',
        'partially_added': '一部追加しました',
        'error': 'エラー',
        
        # Search/Results
        'no_results': '結果なし',
        'search_results': '検索結果',
        'lookup_results': '検索結果',
        
        # Footer messages
        'images_refreshed': '画像を更新しました',
        'buttons_expired': 'ボタンの有効期限が切れました - もう一度コマンドを使用してください',
        
        # Variation footer
        'item_has': 'このアイテムには',
        'variations': 'バリエーション',
        'patterns': 'パターン',
        'and': 'と',
        
        # Variant selector
        'choose_variant': 'バリエーションを選択...',
        'choose_variant_page': 'バリエーションを選択 ({page}/{total}ページ)...',
        
        # Preference dialogs
        'language_updated': '言語が更新されました',
        'language_set_to': 'ご希望の言語が設定されました：',
        'what_this_means': 'これにより',
        'language_benefits': '• アイテム検索があなたの言語の名前と一致します\n• アイテムの詳細があなたの言語で表示されます\n• /lookup は完全対応 — 他のコマンドは対応中です！\n• 英語名でも検索できます',
        'language_update_failed': '言語設定の更新に失敗しました。もう一度お試しください。',
        'language_set': '言語を設定しました！',
        'enjoy_nooklook': '準備完了です！NookLookをお楽しみください。',
        'change_anytime': '/language でいつでも変更できます',
    },
    'zh': {
        # Embed labels
        'category': '类别',
        'sell_price': '卖价',
        'buy_price': '买价',
        'source': '来源',
        'details': '详情',
        'variant': '变体',
        'default': '默认',
        'item_hex': '物品Hex',
        'hex': 'Hex',
        'ti_customize': 'TI自定义',
        'hha_info': 'HHA信息',
        'hha_points': 'HHA点数',
        'customizable': '可定制',
        'bells': '铃钱',
        'variants': '变体',
        'variants_available': '可用',
        
        # Buttons
        'add_to_stash': '添加到收藏',
        'refresh_images': '刷新图片',
        'nookipedia': 'Nookipedia',
        'cancel': '取消',
        'confirm': '确认',
        
        # Stash UI
        'stash': '收藏',
        'item': '物品',
        'quantity': '数量',
        'items': '物品',
        'select_stash': '选择收藏...',
        'stash_full': '收藏已满',
        'added_to_stash': '已添加到收藏',
        'partially_added': '部分已添加',
        'error': '错误',
        
        # Search/Results
        'no_results': '无结果',
        'search_results': '搜索结果',
        'lookup_results': '查找结果',
        
        # Footer messages
        'images_refreshed': '图片已刷新',
        'buttons_expired': '按钮已过期 - 请重新使用命令',
        
        # Variation footer
        'item_has': '此物品有',
        'variations': '种变化',
        'patterns': '种图案',
        'and': '和',
        
        # Variant selector
        'choose_variant': '选择变体...',
        'choose_variant_page': '选择变体 (第{page}/{total}页)...',
        
        # Preference dialogs
        'language_updated': '语言已更新',
        'language_set_to': '您的首选语言现在是',
        'what_this_means': '这意味着',
        'language_benefits': '• 物品搜索将匹配您语言的名称\n• 物品详情将以您的语言显示\n• /lookup 已完全支持 - 其他命令正在开发中！\n• 您也可以使用英文名称搜索',
        'language_update_failed': '更新语言偏好失败。请重试。',
        'language_set': '语言已设置！',
        'enjoy_nooklook': '设置完成！请享受使用NookLook。',
        'change_anytime': '随时使用 /language 更改',
    },
    'ko': {
        # Embed labels
        'category': '카테고리',
        'sell_price': '판매가',
        'buy_price': '구매가',
        'source': '입수 방법',
        'details': '상세',
        'variant': '바리에이션',
        'default': '기본',
        'item_hex': '아이템 Hex',
        'hex': 'Hex',
        'ti_customize': 'TI 커스터마이즈',
        'hha_info': 'HHA 정보',
        'hha_points': 'HHA 포인트',
        'customizable': '커스터마이즈 가능',
        'bells': '벨',
        'variants': '바리에이션',
        'variants_available': '이용 가능',
        
        # Buttons
        'add_to_stash': '보관함에 추가',
        'refresh_images': '이미지 새로고침',
        'nookipedia': 'Nookipedia',
        'cancel': '취소',
        'confirm': '확인',
        
        # Stash UI
        'stash': '보관함',
        'item': '아이템',
        'quantity': '수량',
        'items': '아이템',
        'select_stash': '보관함 선택...',
        'stash_full': '보관함이 가득 참',
        'added_to_stash': '보관함에 추가됨',
        'partially_added': '일부 추가됨',
        'error': '오류',
        
        # Search/Results
        'no_results': '결과 없음',
        'search_results': '검색 결과',
        'lookup_results': '조회 결과',
        
        # Footer messages
        'images_refreshed': '이미지가 새로고침되었습니다',
        'buttons_expired': '버튼이 만료되었습니다 - 명령어를 다시 사용하세요',
        
        # Variation footer
        'item_has': '이 아이템에는',
        'variations': '바리에이션',
        'patterns': '패턴',
        'and': '및',
        
        # Variant selector
        'choose_variant': '바리에이션 선택...',
        'choose_variant_page': '바리에이션 선택 ({page}/{total}페이지)...',
        
        # Preference dialogs
        'language_updated': '언어가 업데이트되었습니다',
        'language_set_to': '선호 언어가 설정되었습니다:',
        'what_this_means': '이것이 의미하는 것',
        'language_benefits': '• 아이템 검색이 귀하의 언어 이름과 일치합니다\n• 아이템 세부 정보가 귀하의 언어로 표시됩니다\n• /lookup 완전 지원 — 다른 명령어는 작업 중입니다!\n• 영어 이름으로도 검색할 수 있습니다',
        'language_update_failed': '언어 설정 업데이트에 실패했습니다. 다시 시도해주세요.',
        'language_set': '언어가 설정되었습니다!',
        'enjoy_nooklook': '설정 완료! NookLook을 즐기세요.',
        'change_anytime': '/language로 언제든지 변경 가능',
    },
    'fr': {
        # Embed labels
        'category': 'Catégorie',
        'sell_price': 'Prix de vente',
        'buy_price': "Prix d'achat",
        'source': 'Source',
        'details': 'Détails',
        'variant': 'Variante',
        'default': 'Par défaut',
        'item_hex': 'Hex objet',
        'hex': 'Hex',
        'ti_customize': 'Personnaliser TI',
        'hha_info': 'Info AJD',
        'hha_points': 'Points AJD',
        'customizable': 'Personnalisable',
        'bells': 'Clochettes',
        'variants': 'Variantes',
        'variants_available': 'disponibles',
        
        # Buttons
        'add_to_stash': 'Ajouter au stock',
        'refresh_images': 'Actualiser images',
        'nookipedia': 'Nookipedia',
        'cancel': 'Annuler',
        'confirm': 'Confirmer',
        
        # Stash UI
        'stash': 'Stock',
        'item': 'Objet',
        'quantity': 'Quantité',
        'items': 'objets',
        'select_stash': 'Choisir un stock...',
        'stash_full': 'Stock plein',
        'added_to_stash': 'Ajouté au stock',
        'partially_added': 'Partiellement ajouté',
        'error': 'Erreur',
        
        # Search/Results
        'no_results': 'Aucun résultat',
        'search_results': 'Résultats de recherche',
        'lookup_results': 'Résultats',
        
        # Footer messages
        'images_refreshed': 'Images actualisées',
        'buttons_expired': 'Les boutons ont expiré - utilisez à nouveau la commande',
        
        # Variation footer
        'item_has': 'Cet objet a',
        'variations': 'variations',
        'patterns': 'motifs',
        'and': 'et',
        
        # Variant selector
        'choose_variant': 'Choisir une variante...',
        'choose_variant_page': 'Choisir variante (Page {page}/{total})...',
        
        # Preference dialogs
        'language_updated': 'Langue mise à jour',
        'language_set_to': 'Votre langue préférée est maintenant',
        'what_this_means': 'Ce que cela signifie',
        'language_benefits': "• Les recherches d'objets correspondront aux noms dans votre langue\n• Les détails des objets s'afficheront dans votre langue\n• /lookup est entièrement pris en charge — d'autres commandes sont en cours !\n• Les noms anglais fonctionnent également",
        'language_update_failed': 'Échec de la mise à jour de la préférence linguistique. Veuillez réessayer.',
        'language_set': 'Langue définie !',
        'enjoy_nooklook': "C'est prêt ! Profitez de NookLook.",
        'change_anytime': 'Modifiable à tout moment avec /language',
    },
    'de': {
        # Embed labels
        'category': 'Kategorie',
        'sell_price': 'Verkaufspreis',
        'buy_price': 'Kaufpreis',
        'source': 'Quelle',
        'details': 'Details',
        'variant': 'Variante',
        'default': 'Standard',
        'item_hex': 'Artikel-Hex',
        'hex': 'Hex',
        'ti_customize': 'TI Anpassen',
        'hha_info': 'HHA-Info',
        'hha_points': 'HHA-Punkte',
        'customizable': 'Anpassbar',
        'bells': 'Sternis',
        'variants': 'Varianten',
        'variants_available': 'verfügbar',
        
        # Buttons
        'add_to_stash': 'Zum Lager hinzufügen',
        'refresh_images': 'Bilder aktualisieren',
        'nookipedia': 'Nookipedia',
        'cancel': 'Abbrechen',
        'confirm': 'Bestätigen',
        
        # Stash UI
        'stash': 'Lager',
        'item': 'Artikel',
        'quantity': 'Menge',
        'items': 'Artikel',
        'select_stash': 'Lager auswählen...',
        'stash_full': 'Lager voll',
        'added_to_stash': 'Zum Lager hinzugefügt',
        'partially_added': 'Teilweise hinzugefügt',
        'error': 'Fehler',
        
        # Search/Results
        'no_results': 'Keine Ergebnisse',
        'search_results': 'Suchergebnisse',
        'lookup_results': 'Ergebnisse',
        
        # Footer messages
        'images_refreshed': 'Bilder aktualisiert',
        'buttons_expired': 'Schaltflächen sind abgelaufen - verwenden Sie den Befehl erneut',
        
        # Variation footer
        'item_has': 'Dieses Objekt hat',
        'variations': 'Variationen',
        'patterns': 'Muster',
        'and': 'und',
        
        # Variant selector
        'choose_variant': 'Variante wählen...',
        'choose_variant_page': 'Variante wählen (Seite {page}/{total})...',
        
        # Preference dialogs
        'language_updated': 'Sprache aktualisiert',
        'language_set_to': 'Ihre bevorzugte Sprache ist jetzt',
        'what_this_means': 'Was das bedeutet',
        'language_benefits': '• Artikelsuchen werden Namen in Ihrer Sprache finden\n• Artikeldetails werden in Ihrer Sprache angezeigt\n• /lookup wird vollständig unterstützt — andere Befehle werden bearbeitet!\n• Englische Namen funktionieren auch',
        'language_update_failed': 'Spracheinstellung konnte nicht aktualisiert werden. Bitte versuchen Sie es erneut.',
        'language_set': 'Sprache festgelegt!',
        'enjoy_nooklook': 'Alles bereit! Viel Spaß mit NookLook.',
        'change_anytime': 'Jederzeit änderbar mit /language',
    },
    'es': {
        # Embed labels
        'category': 'Categoría',
        'sell_price': 'Precio de venta',
        'buy_price': 'Precio de compra',
        'source': 'Fuente',
        'details': 'Detalles',
        'variant': 'Variante',
        'default': 'Por defecto',
        'item_hex': 'Hex del artículo',
        'hex': 'Hex',
        'ti_customize': 'Personalizar TI',
        'hha_info': 'Info ACV',
        'hha_points': 'Puntos ACV',
        'customizable': 'Personalizable',
        'bells': 'Bayas',
        'variants': 'Variantes',
        'variants_available': 'disponibles',
        
        # Buttons
        'add_to_stash': 'Añadir al almacén',
        'refresh_images': 'Actualizar imágenes',
        'nookipedia': 'Nookipedia',
        'cancel': 'Cancelar',
        'confirm': 'Confirmar',
        
        # Stash UI
        'stash': 'Almacén',
        'item': 'Artículo',
        'quantity': 'Cantidad',
        'items': 'artículos',
        'select_stash': 'Elegir almacén...',
        'stash_full': 'Almacén lleno',
        'added_to_stash': 'Añadido al almacén',
        'partially_added': 'Parcialmente añadido',
        'error': 'Error',
        
        # Search/Results
        'no_results': 'Sin resultados',
        'search_results': 'Resultados de búsqueda',
        'lookup_results': 'Resultados',
        
        # Footer messages
        'images_refreshed': 'Imágenes actualizadas',
        'buttons_expired': 'Los botones han caducado - usa el comando de nuevo',
        
        # Variation footer
        'item_has': 'Este objeto tiene',
        'variations': 'variaciones',
        'patterns': 'patrones',
        'and': 'y',
        
        # Variant selector
        'choose_variant': 'Elegir variante...',
        'choose_variant_page': 'Elegir variante (Página {page}/{total})...',
        
        # Preference dialogs
        'language_updated': 'Idioma actualizado',
        'language_set_to': 'Tu idioma preferido ahora es',
        'what_this_means': 'Lo que esto significa',
        'language_benefits': '• Las búsquedas de objetos coincidirán con nombres en tu idioma\n• Los detalles de objetos se mostrarán en tu idioma\n• /lookup es totalmente compatible — ¡otros comandos están en desarrollo!\n• Los nombres en inglés también funcionan',
        'language_update_failed': 'Error al actualizar la preferencia de idioma. Por favor, inténtalo de nuevo.',
        'language_set': '¡Idioma configurado!',
        'enjoy_nooklook': '¡Todo listo! Disfruta de NookLook.',
        'change_anytime': 'Cambia en cualquier momento con /language',
    },
    'it': {
        # Embed labels
        'category': 'Categoria',
        'sell_price': 'Prezzo di vendita',
        'buy_price': 'Prezzo di acquisto',
        'source': 'Fonte',
        'details': 'Dettagli',
        'variant': 'Variante',
        'default': 'Predefinito',
        'item_hex': 'Hex oggetto',
        'hex': 'Hex',
        'ti_customize': 'Personalizza TI',
        'hha_info': 'Info ACA',
        'hha_points': 'Punti ACA',
        'customizable': 'Personalizzabile',
        'bells': 'Stelline',
        'variants': 'Varianti',
        'variants_available': 'disponibili',
        
        # Buttons
        'add_to_stash': 'Aggiungi alla scorta',
        'refresh_images': 'Aggiorna immagini',
        'nookipedia': 'Nookipedia',
        'cancel': 'Annulla',
        'confirm': 'Conferma',
        
        # Stash UI
        'stash': 'Scorta',
        'item': 'Oggetto',
        'quantity': 'Quantità',
        'items': 'oggetti',
        'select_stash': 'Scegli una scorta...',
        'stash_full': 'Scorta piena',
        'added_to_stash': 'Aggiunto alla scorta',
        'partially_added': 'Parzialmente aggiunto',
        'error': 'Errore',
        
        # Search/Results
        'no_results': 'Nessun risultato',
        'search_results': 'Risultati della ricerca',
        'lookup_results': 'Risultati',
        
        # Footer messages
        'images_refreshed': 'Immagini aggiornate',
        'buttons_expired': 'I pulsanti sono scaduti - usa di nuovo il comando',
        
        # Variation footer
        'item_has': 'Questo oggetto ha',
        'variations': 'variazioni',
        'patterns': 'motivi',
        'and': 'e',
        
        # Variant selector
        'choose_variant': 'Scegli variante...',
        'choose_variant_page': 'Scegli variante (Pagina {page}/{total})...',
        
        # Preference dialogs
        'language_updated': 'Lingua aggiornata',
        'language_set_to': 'La tua lingua preferita è ora',
        'what_this_means': 'Cosa significa',
        'language_benefits': '• Le ricerche di oggetti corrisponderanno ai nomi nella tua lingua\n• I dettagli degli oggetti saranno mostrati nella tua lingua\n• /lookup è completamente supportato — altri comandi sono in lavorazione!\n• Funzionano anche le parole in inglese',
        'language_update_failed': 'Impossibile aggiornare la preferenza della lingua. Riprova.',
        'language_set': 'Lingua impostata!',
        'enjoy_nooklook': 'Tutto pronto! Goditi NookLook.',
        'change_anytime': 'Modifica in qualsiasi momento con /language',
    },
    'nl': {
        # Embed labels
        'category': 'Categorie',
        'sell_price': 'Verkoopprijs',
        'buy_price': 'Koopprijs',
        'source': 'Bron',
        'details': 'Details',
        'variant': 'Variant',
        'default': 'Standaard',
        'item_hex': 'Item Hex',
        'hex': 'Hex',
        'ti_customize': 'TI Aanpassen',
        'hha_info': 'HHA-info',
        'hha_points': 'HHA-punten',
        'customizable': 'Aanpasbaar',
        'bells': 'Bells',
        'variants': 'Varianten',
        'variants_available': 'beschikbaar',
        
        # Buttons
        'add_to_stash': 'Toevoegen aan opslag',
        'refresh_images': "Afbeeldingen verversen",
        'nookipedia': 'Nookipedia',
        'cancel': 'Annuleren',
        'confirm': 'Bevestigen',
        
        # Stash UI
        'stash': 'Opslag',
        'item': 'Item',
        'quantity': 'Hoeveelheid',
        'items': 'items',
        'select_stash': 'Kies opslag...',
        'stash_full': 'Opslag vol',
        'added_to_stash': 'Toegevoegd aan opslag',
        'partially_added': 'Gedeeltelijk toegevoegd',
        'error': 'Fout',
        
        # Search/Results
        'no_results': 'Geen resultaten',
        'search_results': 'Zoekresultaten',
        'lookup_results': 'Resultaten',
        
        # Footer messages
        'images_refreshed': 'Afbeeldingen vernieuwd',
        'buttons_expired': 'Knoppen zijn verlopen - gebruik het commando opnieuw',
        
        # Variation footer
        'item_has': 'Dit item heeft',
        'variations': 'variaties',
        'patterns': 'patronen',
        'and': 'en',
        
        # Variant selector
        'choose_variant': 'Kies variant...',
        'choose_variant_page': 'Kies variant (Pagina {page}/{total})...',
        
        # Preference dialogs
        'language_updated': 'Taal bijgewerkt',
        'language_set_to': 'Je voorkeurstaal is nu',
        'what_this_means': 'Wat dit betekent',
        'language_benefits': '• Zoeken naar items komt overeen met namen in jouw taal\n• Itemdetails worden in jouw taal weergegeven\n• /lookup wordt volledig ondersteund — andere commando\'s zijn in ontwikkeling!\n• Engelse namen werken ook',
        'language_update_failed': 'Taalvoorkeur bijwerken mislukt. Probeer het opnieuw.',
        'language_set': 'Taal ingesteld!',
        'enjoy_nooklook': 'Klaar! Veel plezier met NookLook.',
        'change_anytime': 'Wijzig op elk moment met /language',
    },
    'ru': {
        # Embed labels
        'category': 'Категория',
        'sell_price': 'Цена продажи',
        'buy_price': 'Цена покупки',
        'source': 'Источник',
        'details': 'Детали',
        'variant': 'Вариант',
        'default': 'По умолчанию',
        'item_hex': 'Hex предмета',
        'hex': 'Hex',
        'ti_customize': 'TI Настройка',
        'hha_info': 'Инфо HHA',
        'hha_points': 'Очки HHA',
        'customizable': 'Настраиваемый',
        'bells': 'Колокольчики',
        'variants': 'Варианты',
        'variants_available': 'доступно',
        
        # Buttons
        'add_to_stash': 'Добавить в хранилище',
        'refresh_images': 'Обновить изображения',
        'nookipedia': 'Nookipedia',
        'cancel': 'Отмена',
        'confirm': 'Подтвердить',
        
        # Stash UI
        'stash': 'Хранилище',
        'item': 'Предмет',
        'quantity': 'Количество',
        'items': 'предметов',
        'select_stash': 'Выбрать хранилище...',
        'stash_full': 'Хранилище заполнено',
        'added_to_stash': 'Добавлено в хранилище',
        'partially_added': 'Частично добавлено',
        'error': 'Ошибка',
        
        # Search/Results
        'no_results': 'Нет результатов',
        'search_results': 'Результаты поиска',
        'lookup_results': 'Результаты',
        
        # Footer messages
        'images_refreshed': 'Изображения обновлены',
        'buttons_expired': 'Кнопки устарели - используйте команду снова',
        
        # Variation footer
        'item_has': 'Этот предмет имеет',
        'variations': 'вариаций',
        'patterns': 'узоров',
        'and': 'и',
        
        # Variant selector
        'choose_variant': 'Выберите вариант...',
        'choose_variant_page': 'Выберите вариант (Стр. {page}/{total})...',
        
        # Preference dialogs
        'language_updated': 'Язык обновлен',
        'language_set_to': 'Ваш предпочтительный язык теперь',
        'what_this_means': 'Что это значит',
        'language_benefits': '• Поиск предметов будет соответствовать названиям на вашем языке\n• Детали предметов будут отображаться на вашем языке\n• /lookup полностью поддерживается — другие команды в разработке!\n• Английские названия тоже работают',
        'language_update_failed': 'Не удалось обновить языковые настройки. Пожалуйста, попробуйте снова.',
        'language_set': 'Язык установлен!',
        'enjoy_nooklook': 'Готово! Приятного использования NookLook.',
        'change_anytime': 'Изменить в любое время с помощью /language',
    },
}


def get_string(key: str, language: str = 'en') -> str:
    """Get a localized UI string.
    
    Args:
        key: The string key (e.g., 'category', 'add_to_stash')
        language: Language code (e.g., 'en', 'ja', 'fr')
    
    Returns:
        The localized string, or English fallback if not found
    """
    # Get language strings, fallback to English
    lang_strings = UI_STRINGS.get(language, UI_STRINGS['en'])
    
    # Get the string, fallback to English if key missing
    if key in lang_strings:
        return lang_strings[key]
    
    # Fallback to English
    return UI_STRINGS['en'].get(key, key)


def get_strings(language: str = 'en') -> Dict[str, str]:
    """Get all UI strings for a language.
    
    Args:
        language: Language code
    
    Returns:
        Dictionary of all UI strings for that language
    """
    return UI_STRINGS.get(language, UI_STRINGS['en'])


class Localizer:
    """Helper class for localized strings with a fixed language.
    
    Usage:
        loc = Localizer('ja')
        label = loc.get('category')  # Returns 'カテゴリー'
    """
    
    def __init__(self, language: str = 'en'):
        self.language = language
        self._strings = UI_STRINGS.get(language, UI_STRINGS['en'])
        self._fallback = UI_STRINGS['en']
    
    def get(self, key: str) -> str:
        """Get a localized string."""
        return self._strings.get(key, self._fallback.get(key, key))
    
    def __call__(self, key: str) -> str:
        """Shorthand for get()."""
        return self.get(key)


class LocalizedUI:
    """Helper class providing property access to localized UI strings.
    
    Usage:
        ui = get_ui('ja')
        print(ui.category)      # 'カテゴリー'
        print(ui.add_stash)     # '📦 スタッシュに追加'
        print(ui.bells)         # 'ベル'
        print(ui.translate_category('Shoes'))  # 'くつ'
    """
    
    def __init__(self, language: str = 'en'):
        self.language = language
        self._strings = UI_STRINGS.get(language, UI_STRINGS['en'])
        self._fallback = UI_STRINGS['en']
    
    def _get(self, key: str) -> str:
        """Get a localized string with fallback."""
        return self._strings.get(key, self._fallback.get(key, key))
    
    def translate_category(self, category: str) -> str:
        """Translate a category name."""
        return translate_category(category, self.language)
    
    def translate_source(self, source: str) -> str:
        """Translate a source name."""
        return translate_source(source, self.language)
    
    # Embed labels
    @property
    def category(self) -> str:
        return self._get('category')
    
    @property
    def sell_price(self) -> str:
        return self._get('sell_price')
    
    @property
    def buy_price(self) -> str:
        return self._get('buy_price')
    
    @property
    def source(self) -> str:
        return self._get('source')
    
    @property
    def details(self) -> str:
        return self._get('details')
    
    @property
    def variant(self) -> str:
        return self._get('variant')
    
    @property
    def default(self) -> str:
        return self._get('default')
    
    @property
    def item_hex(self) -> str:
        return self._get('item_hex')
    
    @property
    def hex(self) -> str:
        return self._get('hex')
    
    @property
    def hha_info(self) -> str:
        return self._get('hha_info')
    
    @property
    def hha_points(self) -> str:
        return self._get('hha_points')
    
    @property
    def customizable(self) -> str:
        return self._get('customizable')
    
    @property
    def bells(self) -> str:
        return self._get('bells')
    
    @property
    def variants(self) -> str:
        return self._get('variants')
    
    @property
    def variants_available(self) -> str:
        return self._get('variants_available')
    
    # Buttons (with emoji prefixes for display)
    @property
    def add_stash(self) -> str:
        return f"📦 {self._get('add_to_stash')}"
    
    @property
    def refresh(self) -> str:
        return f"🔄 {self._get('refresh_images')}"
    
    @property
    def nookipedia(self) -> str:
        return self._get('nookipedia')
    
    @property
    def cancel(self) -> str:
        return self._get('cancel')
    
    @property
    def confirm(self) -> str:
        return self._get('confirm')
    
    # Messages
    @property
    def no_results(self) -> str:
        return self._get('no_results')
    
    @property
    def error(self) -> str:
        return self._get('error')
    
    @property
    def stash_full(self) -> str:
        return self._get('stash_full')
    
    @property
    def added_to_stash(self) -> str:
        return self._get('added_to_stash')
    
    # Footer messages
    @property
    def images_refreshed(self) -> str:
        return f"🔄 {self._get('images_refreshed')}"
    
    @property
    def buttons_expired(self) -> str:
        return f"💤 {self._get('buttons_expired')}"
    
    # Variation footer
    @property
    def item_has(self) -> str:
        return self._get('item_has')
    
    @property
    def variations_word(self) -> str:
        return self._get('variations')
    
    @property
    def patterns_word(self) -> str:
        return self._get('patterns')
    
    @property
    def and_word(self) -> str:
        return self._get('and')
    
    def format_variation_footer(self, variation_count: int = 0, pattern_count: int = 0, total_variants: int = 0) -> str:
        """Format the variation footer text.
        
        Args:
            variation_count: Number of variations (colors/styles)
            pattern_count: Number of patterns (designs)
            total_variants: Total variant count (fallback if no variations/patterns)
        
        Returns:
            Localized footer like "This item has 7 variations and 4 patterns"
        """
        parts = []
        if variation_count > 1:
            parts.append(f"{variation_count} {self.variations_word}")
        if pattern_count > 1:
            parts.append(f"{pattern_count} {self.patterns_word}")
        
        if parts:
            summary = f" {self.and_word} ".join(parts)
        elif total_variants > 1:
            # Fallback to total variant count
            summary = f"{total_variants} {self.variants}"
        else:
            return ""
        
        return f"{self.item_has} {summary}"
    
    def format_variants_available(self, variation_count: int = 0, pattern_count: int = 0, total_variants: int = 0) -> str:
        """Format 'X variations available' or 'X variations and Y patterns' for embed field.
        
        Args:
            variation_count: Number of unique variations
            pattern_count: Number of unique patterns  
            total_variants: Total variant count (fallback)
        
        Returns:
            Localized string like "8 variations available" or "7 variations and 4 patterns"
        """
        parts = []
        if variation_count > 1:
            parts.append(f"{variation_count} {self.variations_word}")
        if pattern_count > 1:
            parts.append(f"{pattern_count} {self.patterns_word}")
        
        if parts:
            summary = f" {self.and_word} ".join(parts)
        elif total_variants > 1:
            summary = f"{total_variants} {self.variants}"
        else:
            return ""
        
        return f"{summary} {self.variants_available}"
    
    # Variant selector
    @property
    def choose_variant(self) -> str:
        return self._get('choose_variant')
    
    def choose_variant_page(self, page: int, total: int) -> str:
        """Get localized 'Choose variant (Page X/Y)...' placeholder."""
        template = self._get('choose_variant_page')
        return template.format(page=page, total=total)
    
    # Preference dialogs
    @property
    def language_updated(self) -> str:
        return self._get('language_updated')
    
    @property
    def language_set_to(self) -> str:
        return self._get('language_set_to')
    
    @property
    def what_this_means(self) -> str:
        return self._get('what_this_means')
    
    @property
    def language_benefits(self) -> str:
        return self._get('language_benefits')
    
    @property
    def language_update_failed(self) -> str:
        return self._get('language_update_failed')
    
    @property
    def language_set(self) -> str:
        return self._get('language_set')
    
    @property
    def enjoy_nooklook(self) -> str:
        return self._get('enjoy_nooklook')
    
    @property
    def change_anytime(self) -> str:
        return self._get('change_anytime')


def get_ui(language: str = 'en') -> LocalizedUI:
    """Get a LocalizedUI helper for the specified language.
    
    Args:
        language: Language code (e.g., 'en', 'ja', 'fr')
    
    Returns:
        LocalizedUI instance for property-based access to strings
    
    Example:
        ui = get_ui('ja')
        embed.add_field(name=ui.details, value="...")
        button.label = ui.add_stash
    """
    return LocalizedUI(language)
