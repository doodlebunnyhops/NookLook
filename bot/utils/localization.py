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
        'Other': 'その他',
        'Ceiling Decor': 'てんじょう',
        'ceiling-decor': 'てんじょう',
        'Interior Structures': 'けんちく',
        'interior-structures': 'けんちく',
        'Equipment': 'そうび',
        'Savory': 'しょっぱい',
        'Sweet': 'あまい',
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
        'Other': '其他',
        'Ceiling Decor': '天花板装饰',
        'ceiling-decor': '天花板装饰',
        'Interior Structures': '室内结构',
        'interior-structures': '室内结构',
        'Equipment': '装备',
        'Savory': '咸食',
        'Sweet': '甜食',
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
        'Other': '기타',
        'Ceiling Decor': '천장 장식',
        'ceiling-decor': '천장 장식',
        'Interior Structures': '실내 구조물',
        'interior-structures': '실내 구조물',
        'Equipment': '장비',
        'Savory': '짭은 음식',
        'Sweet': '달콤한 음식',
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
        'Other': 'Autres',
        'Ceiling Decor': 'Décor de plafond',
        'ceiling-decor': 'Décor de plafond',
        'Interior Structures': 'Structures intérieures',
        'interior-structures': 'Structures intérieures',
        'Equipment': 'Équipement',
        'Savory': 'Salé',
        'Sweet': 'Sucré',
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
        'Other': 'Sonstiges',
        'Ceiling Decor': 'Deckendekor',
        'ceiling-decor': 'Deckendekor',
        'Interior Structures': 'Innenstrukturen',
        'interior-structures': 'Innenstrukturen',
        'Equipment': 'Ausrüstung',
        'Savory': 'Herzhaft',
        'Sweet': 'Süß',
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
        'Other': 'Otros',
        'Ceiling Decor': 'Decoración de techo',
        'ceiling-decor': 'Decoración de techo',
        'Interior Structures': 'Estructuras interiores',
        'interior-structures': 'Estructuras interiores',
        'Equipment': 'Equipamiento',
        'Savory': 'Salado',
        'Sweet': 'Dulce',
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
        'Other': 'Altro',
        'Ceiling Decor': 'Decorazioni da soffitto',
        'ceiling-decor': 'Decorazioni da soffitto',
        'Interior Structures': 'Strutture interne',
        'interior-structures': 'Strutture interne',
        'Equipment': 'Attrezzatura',
        'Savory': 'Salato',
        'Sweet': 'Dolce',
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
        'Other': 'Overig',
        'Ceiling Decor': 'Plafonddecoratie',
        'ceiling-decor': 'Plafonddecoratie',
        'Interior Structures': 'Binnenstructuren',
        'interior-structures': 'Binnenstructuren',
        'Equipment': 'Uitrusting',
        'Savory': 'Hartig',
        'Sweet': 'Zoet',
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
        'Other': 'Другое',
        'Ceiling Decor': 'Потолочный декор',
        'ceiling-decor': 'Потолочный декор',
        'Interior Structures': 'Внутренние структуры',
        'interior-structures': 'Внутренние структуры',
        'Equipment': 'Снаряжение',
        'Savory': 'Солёное',
        'Sweet': 'Сладкое',
    },
}

# Source translations (English -> localized)
# These are common ACNH item sources
SOURCE_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'ja': {
        # NPCs
        'Able Sisters': 'エイブルシスターズ',
        'All villagers': 'すべてのじゅうみん',
        'Blathers': 'フータ',
        'Brewster': 'マスター',
        'C.J.': 'ジャスティン',
        'Celeste': 'フーコ',
        'Cyrus': 'カイゾー',
        'Daisy Mae': 'ウリ',
        'Flick': 'レックス',
        'Franklin': 'フランクリン',
        'Gullivarrr': 'かいぞく',
        'Gulliver': 'ジョニー',
        'Harvey': 'パニエル',
        'HHA': 'ハッピーホームアカデミー',
        'Isabelle': 'しずえ',
        'Jack': 'パンプキング',
        'Jingle': 'ジングル',
        'K.K.': 'とたけけ',
        'Kapp\'n': 'かっぺい',
        'Katrina': 'ハッケミィ',
        'Kicks': 'シャンク',
        'Label': 'ことの',
        'Leif': 'レイジ',
        'Lottie': 'タクミ',
        'Luna': 'ゆめみ',
        'Mom': 'はは',
        'Niko': 'ニコ',
        'Nintendo': '任天堂',
        'Pascal': 'ラコスケ',
        'Pavé': 'ベルリーナ',
        'Redd': 'つねきち',
        'Reese': 'リサ',
        'Rover': 'みしらぬネコ',
        'Saharah': 'ローラン',
        'Snowboy': 'ゆきだるま',
        'Tom Nook': 'たぬきち',
        'Wardell': 'ナッティー',
        'Wilbur': 'ロドリー',
        'Wisp': 'ゆうたろう',
        'Zipper': 'ぴょんたろう',
        # Villager types
        'Big Sister villagers': 'アネキけいじゅうみん',
        'Cranky villagers': 'コワイけいじゅうみん',
        'Jock villagers': 'ハキハキけいじゅうみん',
        # Activities
        'Assessing fossils': 'かせきのかんてい',
        'Balloon': 'ふうせん',
        'Balloons': 'ふうせん',
        'Beach': 'ビーチ',
        'Birthday': 'たんじょうび',
        'Breeding': 'こうはい',
        'Bug catching': 'ムシとり',
        'Clam dig spot': 'アサリほりポイント',
        'Cooking': 'りょうり',
        'Crafting': 'DIY',
        'Dig Spot': 'ほりポイント',
        'Dive spot': 'ダイブポイント',
        'Diving': 'そせん',
        'Dodo Airlines': 'ドードーエアラインズ',
        'Egg balloon': 'エッグふうせん',
        'Egg balloons': 'エッグふうせん',
        'Egg bottles': 'エッグボトル',
        'Expired turnips': 'くさったカブ',
        'Fishing': 'つり',
        'Glowing dig spot': 'ひかるほりポイント',
        'Gold balloon': 'きんのふうせん',
        'Group Stretching': 'ラジオたいそう',
        'High Friendship': 'こうこうかんど',
        'Hitting a rock': 'いわをたたく',
        'K.K. concert': 'とたけけライブ',
        'Kapp\'n islands': 'かっぺいツアー',
        'Mail': 'てがみ',
        'May Day Tour': 'メーデーツアー',
        'NookLink': 'タヌポータル',
        'Nook Miles Redemption': 'マイルりょうきん',
        'Nook Shopping': 'たぬきショッピング',
        'Nook Shopping Daily Selection': 'たぬきショッピング(ひがわり)',
        'Nook Shopping Posters': 'たぬきショッピング(ポスター)',
        'Nook Shopping Promotion': 'たぬきショッピング(げんてい)',
        'Nook Shopping Seasonal': 'たぬきショッピング(きせつ)',
        'Nook\'s Cranny': 'たぬきショップ',
        'NotAvailable': '入手不可',
        'On ground': 'じめんのうえ',
        'Picking flowers': 'はなつみ',
        'Recycle box': 'リサイクルボックス',
        'Redd\'s Co-op Raffle': 'つねきちくじ',
        'Redd\'s Raffle': 'つねきちくじ',
        'Seed bag': 'たねぶくろ',
        'Shaking a hardwood or cedar tree': 'きをゆする',
        'Starting items': 'はじめのアイテム',
        'Wishing on shooting stars': 'ほしにねがいを',
        'Wrapping a present': 'ラッピング',
        'Wrapping bells': 'ベルをつつむ',
        # Shops
        'HHP Apparel Shop': 'HHPアパレルショップ',
        'HHP Café': 'HHPカフェ',
        'HHP Office': 'HHPオフィス',
        'Jolly Redd\'s Treasure Trawler': 'いなりマーケット',
        'Katrina\'s Cleansing Service': 'ハッケミィおはらい',
        'Kicks\' Co-op': 'シャンクきょうどう',
        'Redd\'s Co-op Raffle': 'つねきちきょうどうくじ',
        'Saharah\'s Co-op': 'ローランきょうどう',
        # Trees
        'Apple Tree': 'リンゴのき',
        'Cedar Tree': 'スギのき',
        'Cherry Tree': 'サクランボのき',
        'Orange Tree': 'オレンジのき',
        'Peach Tree': 'モモのき',
        'Pear Tree': 'ナシのき',
        # Recipe books
        'Basic Cooking Recipes': 'きほんのりょうりレシピ',
        'Be a Chef! DIY Recipes+': 'シェフになろう！DIYレシピ+',
        'Cozy Turkey Day DIY': 'サンクスギビングDIY',
        'Custom Fencing in a Flash': 'カスタムさくレシピ',
        'DIY for Beginners': 'はじめてのDIYレシピ',
        # Misc activities  
        'Breaking 100 axes': 'オノを100かいこわす',
        'Burying bells in a glowing spot': 'ひかるほりポイントにベル',
        'Catching a barred knifejaw': 'イシダイをつる',
        'Catching a blue marlin': 'カジキをつる',
        'Catching a dab': 'カレイをつる',
        'Catching a horse mackerel': 'アジをつる',
        'Catching a olive flounder': 'ヒラメをつる',
        'Catching a red snapper': 'タイをつる',
        'Catching a salmon': 'サケをつる',
        'Catching a sea bass': 'スズキをつる',
        'Catching a squid': 'イカをつる',
        'Catching an anchovy': 'アンチョビをつる',
        'Catching with a net': 'アミでとる',
        'Check Toy Day stockings the day after Toy Day': 'トイデーのよくじつ',
        'Chopping a bamboo tree': 'タケをきる',
        'Chopping a tree': 'きをきる',
        'Collecting earth eggs': 'じめんのたまごあつめ',
        'Collecting leaf eggs': 'はっぱのたまごあつめ',
        'Collecting sky eggs': 'そらとぶたまごあつめ',
        'Collecting stone eggs': 'いわのたまごあつめ',
        'Collecting water eggs': 'さかなのたまごあつめ',
        'Collecting wood eggs': 'ウッディなたまごあつめ',
        'Completing bug Critterpedia': 'ムシずかんコンプリート',
        'Completing fish Critterpedia': 'さかなずかんコンプリート',
        'Delivering item for a villager': 'じゅうみんのおとどけもの',
        'Digging up a carrot plant': 'ニンジンをほる',
        'Digging up a fully grown bush': 'ていぼくをほる',
        'Digging up a potato plant': 'ジャガイモをほる',
        'Digging up a pumpkin plant': 'カボチャをほる',
        'Digging up a sugarcane plant': 'サトウキビをほる',
        'Digging up a tomato plant': 'トマトをほる',
        'Digging up a wheat plant': 'コムギをほる',
        'Digging up clams': 'アサリをほる',
        'Don\'t return lost item': 'おとしものをかえさない',
        'Don\'t return treasure quest item': 'たからさがしをかえさない',
        'Donating all art': 'びじゅつひんコンプリート',
        'Donating all bugs': 'ムシコンプリート',
        'Donating all fish': 'さかなコンプリート',
        'Donating all fossils': 'かせきコンプリート',
        'Donating all sea creatures': 'うみのさちコンプリート',
        'Helping Gulliver 30 times': 'ジョニー30かいてつだう',
        'Picking carrots': 'ニンジンしゅうかく',
        'Picking potatoes': 'ジャガイモしゅうかく',
        'Picking pumpkins': 'カボチャしゅうかく',
        'Picking sugarcane': 'サトウキビしゅうかく',
        'Picking tomatoes': 'トマトしゅうかく',
        'Picking wheat': 'コムギしゅうかく',
        'Planting a bamboo shoot': 'タケのこをうえる',
        'Planting a cedar sapling': 'スギのなえをうえる',
        'Planting a cherry': 'サクランボをうえる',
        'Planting a coconut': 'ヤシのみをうえる',
        'Planting a peach': 'モモをうえる',
        'Planting a pear': 'ナシをうえる',
        'Planting a sapling': 'なえをうえる',
        'Planting an apple': 'リンゴをうえる',
        'Planting an orange': 'オレンジをうえる',
        'Use a fountain firework': 'ふんすいはなびをつかう',
        # Status conditions
        '5-star town status': '5つぼしのしま',
        'while stung': 'ハチにさされたとき',
        # Donation unlocks
        'unlocked after 100 donations': '100こきふでかいほう',
        'unlocked after 20 donations': '20こきふでかいほう',
        'unlocked after 40 donations': '40こきふでかいほう',
        'unlocked after 50 donations': '50こきふでかいほう',
        'unlocked after 5 donations': '5こきふでかいほう',
        'unlocked after 80 donations': '80こきふでかいほう',
    },
    'zh': {
        # NPCs
        'Able Sisters': '服装店',
        'All villagers': '所有居民',
        'Blathers': '傅达',
        'Brewster': '巴猎',
        'C.J.': '俞司廷',
        'Celeste': '傅珂',
        'Cyrus': '健兆',
        'Daisy Mae': '曹卖',
        'Flick': '龙克斯',
        'Franklin': '富兰克林',
        'Gullivarrr': '海盗吕游',
        'Gulliver': '吕游',
        'Harvey': '巴猎',
        'HHA': '快乐家协会',
        'Isabelle': '西施惠',
        'Jack': '南瓜王',
        'Jingle': '麋鹿',
        'K.K.': 'K.K.',
        'Kapp\'n': '航平',
        'Katrina': '夏悟姐',
        'Kicks': '薛革',
        'Label': '绢儿',
        'Leif': '然然',
        'Lottie': '莉咏',
        'Luna': '梦美',
        'Mom': '妈妈',
        'Niko': '阿升',
        'Nintendo': '任天堂',
        'Pascal': '阿獭',
        'Pavé': '孔雀哥哥',
        'Redd': '狐利',
        'Reese': '丽莎',
        'Rover': '巧虎',
        'Saharah': '骆岚',
        'Snowboy': '雪人',
        'Tom Nook': '狸克',
        'Wardell': '华乐迪',
        'Wilbur': '莫里',
        'Wisp': '幽幽',
        'Zipper': '蹦蹦',
        # Activities
        'Balloon': '气球',
        'Balloons': '气球',
        'Beach': '海滩',
        'Birthday': '生日',
        'Bug catching': '捕虫',
        'Cooking': '烹饪',
        'Crafting': 'DIY',
        'Diving': '潜水',
        'Fishing': '钓鱼',
        'Mail': '邮件',
        'Nook Miles Redemption': '里程兑换',
        'Nook Shopping': '狸端机',
        'Nook\'s Cranny': '狸猫商店',
        'NotAvailable': '不可获得',
    },
    'ko': {
        # NPCs
        'Able Sisters': '에이블 시스터즈',
        'All villagers': '모든 주민',
        'Blathers': '부엉',
        'Brewster': '마스터',
        'C.J.': '저스틴',
        'Celeste': '부코',
        'Cyrus': '리포',
        'Daisy Mae': '무파',
        'Flick': '레오',
        'Franklin': '프랭클린',
        'Gullivarrr': '해적 조니',
        'Gulliver': '조니',
        'Harvey': '하비',
        'HHA': '해피홈아카데미',
        'Isabelle': '여울',
        'Jack': '호박왕',
        'Jingle': '징글',
        'K.K.': 'K.K.',
        'Kapp\'n': '갓파',
        'Katrina': '칠성이',
        'Kicks': '슈샹크',
        'Label': '고순이',
        'Leif': '레이지',
        'Lottie': '타쿠미',
        'Luna': '몽몽',
        'Mom': '엄마',
        'Niko': '니코',
        'Nintendo': '닌텐도',
        'Pascal': '라코스케',
        'Pavé': '파베',
        'Redd': '여우네',
        'Reese': '리사',
        'Rover': '냥로그',
        'Saharah': '사막',
        'Snowboy': '눈사람',
        'Tom Nook': '너굴',
        'Wardell': '워델',
        'Wilbur': '윌버',
        'Wisp': '부우',
        'Zipper': '토빗',
        # Activities
        'Balloon': '풍선',
        'Balloons': '풍선',
        'Beach': '해변',
        'Birthday': '생일',
        'Bug catching': '곤충 채집',
        'Cooking': '요리',
        'Crafting': 'DIY',
        'Diving': '잠수',
        'Fishing': '낚시',
        'Mail': '우편',
        'Nook Miles Redemption': '마일 교환',
        'Nook Shopping': '너굴 쇼핑',
        'Nook\'s Cranny': '너굴 상점',
        'NotAvailable': '획득 불가',
    },
    'fr': {
        # NPCs
        'Able Sisters': 'Boutique des sœurs Doigts de fée',
        'All villagers': 'Tous les habitants',
        'Blathers': 'Thibou',
        'Brewster': 'Robusto',
        'C.J.': 'Casimar',
        'Celeste': 'Céleste',
        'Cyrus': 'Serge',
        'Daisy Mae': 'Porcelette',
        'Flick': 'Djason',
        'Franklin': 'Dindo',
        'Gullivarrr': 'Gulliver (pirate)',
        'Gulliver': 'Gulliver',
        'Harvey': 'Joe',
        'HHA': 'AJD',
        'Isabelle': 'Marie',
        'Jack': 'Jack',
        'Jingle': 'Yoann',
        'K.K.': 'Kéké',
        'Kapp\'n': 'Amiral',
        'Katrina': 'Astrid',
        'Kicks': 'Blaise',
        'Label': 'Layette',
        'Leif': 'Racine',
        'Lottie': 'Lou',
        'Luna': 'Serena',
        'Mom': 'Maman',
        'Niko': 'Niko',
        'Nintendo': 'Nintendo',
        'Pascal': 'Pascal',
        'Pavé': 'Pavé',
        'Redd': 'Rounard',
        'Reese': 'Risette',
        'Rover': 'Charly',
        'Saharah': 'Sahara',
        'Snowboy': 'Yétiti',
        'Tom Nook': 'Tom Nook',
        'Wardell': 'Renato',
        'Wilbur': 'Rodrigue',
        'Wisp': 'Spectre',
        'Zipper': 'Albin',
        # Villager types
        'Big Sister villagers': 'Grandes sœurs',
        'Cranky villagers': 'Grognons',
        'Jock villagers': 'Sportifs',
        # Activities
        'Balloon': 'Ballon',
        'Balloons': 'Ballons',
        'Beach': 'Plage',
        'Birthday': 'Anniversaire',
        'Bug catching': 'Chasse aux insectes',
        'Cooking': 'Cuisine',
        'Crafting': 'Bricolage',
        'Diving': 'Plongée',
        'Fishing': 'Pêche',
        'Mail': 'Courrier',
        'Nook Miles Redemption': 'Échange de Miles Nook',
        'Nook Shopping': 'Nook Shopping',
        'Nook Shopping Daily Selection': 'Nook Shopping (quotidien)',
        'Nook Shopping Seasonal': 'Nook Shopping (saisonnier)',
        'Nook\'s Cranny': 'Boutique Nook',
        'NotAvailable': 'Non disponible',
        'Recycle box': 'Bac de recyclage',
    },
    'de': {
        # NPCs
        'Able Sisters': 'Schneiderei',
        'All villagers': 'Alle Bewohner',
        'Blathers': 'Eugen',
        'Brewster': 'Kofi',
        'C.J.': 'Lomeus',
        'Celeste': 'Eufemia',
        'Cyrus': 'Björn',
        'Daisy Mae': 'Jorna',
        'Flick': 'Carlson',
        'Franklin': 'Frank',
        'Gullivarrr': 'Gullivarrr',
        'Gulliver': 'Gulliver',
        'Harvey': 'Harwey',
        'HHA': 'HHA',
        'Isabelle': 'Melinda',
        'Jack': 'Jens',
        'Jingle': 'Renato',
        'K.K.': 'K.K.',
        'Kapp\'n': 'Käpten',
        'Katrina': 'Smeralda',
        'Kicks': 'Schuhbert',
        'Label': 'Tina',
        'Leif': 'Gerd',
        'Lottie': 'Lotte',
        'Luna': 'Serenada',
        'Mom': 'Mama',
        'Niko': 'Niko',
        'Nintendo': 'Nintendo',
        'Pascal': 'Johannes',
        'Pavé': 'Pavé',
        'Redd': 'Reiner',
        'Reese': 'Rosina',
        'Rover': 'Kater',
        'Saharah': 'Saharah',
        'Snowboy': 'Schneemann',
        'Tom Nook': 'Tom Nook',
        'Wardell': 'Oleg',
        'Wilbur': 'Bodo',
        'Wisp': 'Buhu',
        'Zipper': 'Ohs',
        # Villager types
        'Big Sister villagers': 'Große Schwestern',
        'Cranky villagers': 'Mürrische',
        'Jock villagers': 'Sportler',
        # Activities
        'Balloon': 'Ballon',
        'Balloons': 'Ballons',
        'Beach': 'Strand',
        'Birthday': 'Geburtstag',
        'Bug catching': 'Insektenfang',
        'Cooking': 'Kochen',
        'Crafting': 'Heimwerken',
        'Diving': 'Tauchen',
        'Fishing': 'Angeln',
        'Mail': 'Post',
        'Nook Miles Redemption': 'Nook-Meilen-Tausch',
        'Nook Shopping': 'Nook Shopping',
        'Nook Shopping Daily Selection': 'Nook Shopping (täglich)',
        'Nook Shopping Seasonal': 'Nook Shopping (saisonal)',
        'Nook\'s Cranny': 'Nooks Laden',
        'NotAvailable': 'Nicht verfügbar',
        'Recycle box': 'Recyclingbox',
    },
    'es': {
        # NPCs
        'Able Sisters': 'Hermanas Manitas',
        'All villagers': 'Todos los vecinos',
        'Blathers': 'Sócrates',
        'Brewster': 'Fígaro',
        'C.J.': 'C.J.',
        'Celeste': 'Estela',
        'Cyrus': 'Al',
        'Daisy Mae': 'Juliana',
        'Flick': 'Kamilo',
        'Franklin': 'Beniján',
        'Gullivarrr': 'Gullivarrr',
        'Gulliver': 'Gulliver',
        'Harvey': 'Harvey',
        'HHA': 'ACV',
        'Isabelle': 'Canela',
        'Jack': 'Caco',
        'Jingle': 'Renaldo',
        'K.K.': 'Totakeke',
        'Kapp\'n': 'Capitán',
        'Katrina': 'Katrina',
        'Kicks': 'Betunio',
        'Label': 'Trini',
        'Leif': 'Gandulio',
        'Lottie': 'Nuria',
        'Luna': 'Alakama',
        'Mom': 'Mamá',
        'Niko': 'Niko',
        'Nintendo': 'Nintendo',
        'Pascal': 'Pascal',
        'Pavé': 'Pavé',
        'Redd': 'Ladino',
        'Reese': 'Paca',
        'Rover': 'Feli',
        'Saharah': 'Saharah',
        'Snowboy': 'Muñeco de nieve',
        'Tom Nook': 'Tom Nook',
        'Wardell': 'Nando',
        'Wilbur': 'Wilbur',
        'Wisp': 'Buh',
        'Zipper': 'Coti',
        # Villager types
        'Big Sister villagers': 'Hermanas mayores',
        'Cranky villagers': 'Gruñones',
        'Jock villagers': 'Deportistas',
        # Activities
        'Balloon': 'Globo',
        'Balloons': 'Globos',
        'Beach': 'Playa',
        'Birthday': 'Cumpleaños',
        'Bug catching': 'Caza de bichos',
        'Cooking': 'Cocina',
        'Crafting': 'Bricolaje',
        'Diving': 'Buceo',
        'Fishing': 'Pesca',
        'Mail': 'Correo',
        'Nook Miles Redemption': 'Canje de millas Nook',
        'Nook Shopping': 'Nook Shopping',
        'Nook Shopping Daily Selection': 'Nook Shopping (diario)',
        'Nook Shopping Seasonal': 'Nook Shopping (estacional)',
        'Nook\'s Cranny': 'Tienda Nook',
        'NotAvailable': 'No disponible',
        'Recycle box': 'Caja de reciclaje',
    },
    'it': {
        # NPCs
        'Able Sisters': 'Ago e Filo',
        'All villagers': 'Tutti gli abitanti',
        'Blathers': 'Blatero',
        'Brewster': 'Bartolo',
        'C.J.': 'Camelot',
        'Celeste': 'Celeste',
        'Cyrus': 'Alpaca',
        'Daisy Mae': 'Brunella',
        'Flick': 'Volpolo',
        'Franklin': 'Sfondone',
        'Gullivarrr': 'Gullivarrr',
        'Gulliver': 'Gulliver',
        'Harvey': 'Fiorilio',
        'HHA': 'ACA',
        'Isabelle': 'Fuffi',
        'Jack': 'Fifone',
        'Jingle': 'Jingle',
        'K.K.': 'K.K.',
        'Kapp\'n': 'Remo',
        'Katrina': 'Katrina',
        'Kicks': 'Sciuscià',
        'Label': 'Beatrice',
        'Leif': 'Florindo',
        'Lottie': 'Ivana',
        'Luna': 'Sonia',
        'Mom': 'Mamma',
        'Niko': 'Niko',
        'Nintendo': 'Nintendo',
        'Pascal': 'Pascal',
        'Pavé': 'Pavé',
        'Redd': 'Volpolo',
        'Reese': 'Merino',
        'Rover': 'Romeo',
        'Saharah': 'Sahara',
        'Snowboy': 'Pupazzo di neve',
        'Tom Nook': 'Tom Nook',
        'Wardell': 'Foffo',
        'Wilbur': 'Wilbur',
        'Wisp': 'Svanilio',
        'Zipper': 'Ovidio',
        # Villager types
        'Big Sister villagers': 'Sorelle maggiori',
        'Cranky villagers': 'Burberi',
        'Jock villagers': 'Sportivi',
        # Activities
        'Balloon': 'Palloncino',
        'Balloons': 'Palloncini',
        'Beach': 'Spiaggia',
        'Birthday': 'Compleanno',
        'Bug catching': 'Caccia agli insetti',
        'Cooking': 'Cucina',
        'Crafting': 'Fai da te',
        'Diving': 'Immersione',
        'Fishing': 'Pesca',
        'Mail': 'Posta',
        'Nook Miles Redemption': 'Riscatto Miglia Nook',
        'Nook Shopping': 'Nook Shopping',
        'Nook Shopping Daily Selection': 'Nook Shopping (giornaliero)',
        'Nook Shopping Seasonal': 'Nook Shopping (stagionale)',
        'Nook\'s Cranny': 'Bottega di Nook',
        'NotAvailable': 'Non disponibile',
        'Recycle box': 'Cassonetto riciclaggio',
    },
    'nl': {
        # NPCs
        'Able Sisters': 'Able-zusters',
        'All villagers': 'Alle bewoners',
        'Blathers': 'Blansen',
        'Brewster': 'Röster',
        'C.J.': 'C.J.',
        'Celeste': 'Celeste',
        'Cyrus': 'Cyrus',
        'Daisy Mae': 'Lizette',
        'Flick': 'Flink',
        'Franklin': 'Franklin',
        'Gullivarrr': 'Gullivarrr',
        'Gulliver': 'Gulliver',
        'Harvey': 'Harvey',
        'HHA': 'HHA',
        'Isabelle': 'Isabelle',
        'Jack': 'Jason',
        'Jingle': 'Jansen',
        'K.K.': 'K.K.',
        'Kapp\'n': 'Käpp\'n',
        'Katrina': 'Katrina',
        'Kicks': 'Schoensen',
        'Label': 'Lara',
        'Leif': 'Leif',
        'Lottie': 'Karlijn',
        'Luna': 'Serena',
        'Mom': 'Mama',
        'Niko': 'Niko',
        'Nintendo': 'Nintendo',
        'Pascal': 'Pascal',
        'Pavé': 'Pavé',
        'Redd': 'Ransen',
        'Reese': 'Rosalie',
        'Rover': 'Robert',
        'Saharah': 'Saharah',
        'Snowboy': 'Sneeuwpop',
        'Tom Nook': 'Tom Nook',
        'Wardell': 'Wardell',
        'Wilbur': 'Wilbur',
        'Wisp': 'Geertje',
        'Zipper': 'Zipper',
        # Activities
        'Balloon': 'Ballon',
        'Balloons': 'Ballonnen',
        'Beach': 'Strand',
        'Birthday': 'Verjaardag',
        'Bug catching': 'Insecten vangen',
        'Cooking': 'Koken',
        'Crafting': 'Knutselen',
        'Diving': 'Duiken',
        'Fishing': 'Vissen',
        'Mail': 'Post',
        'Nook Miles Redemption': 'Nook Miles inwisselen',
        'Nook Shopping': 'Nook Shopping',
        'Nook\'s Cranny': 'Nooks Winkel',
        'NotAvailable': 'Niet beschikbaar',
        'Recycle box': 'Recyclebak',
    },
    'ru': {
        # NPCs
        'Able Sisters': 'Сёстры Эйбл',
        'All villagers': 'Все жители',
        'Blathers': 'Блезерс',
        'Brewster': 'Брюстер',
        'C.J.': 'К.Д.',
        'Celeste': 'Селеста',
        'Cyrus': 'Сайрус',
        'Daisy Mae': 'Дэйзи Мэй',
        'Flick': 'Флик',
        'Franklin': 'Франклин',
        'Gullivarrr': 'Пират Гулливер',
        'Gulliver': 'Гулливер',
        'Harvey': 'Харви',
        'HHA': 'ДСК',
        'Isabelle': 'Изабель',
        'Jack': 'Джек',
        'Jingle': 'Джингл',
        'K.K.': 'К.К.',
        'Kapp\'n': 'Капитан',
        'Katrina': 'Катрина',
        'Kicks': 'Кикс',
        'Label': 'Лейбл',
        'Leif': 'Лейф',
        'Lottie': 'Лотти',
        'Luna': 'Луна',
        'Mom': 'Мама',
        'Niko': 'Нико',
        'Nintendo': 'Nintendo',
        'Pascal': 'Паскаль',
        'Pavé': 'Павлин',
        'Redd': 'Редд',
        'Reese': 'Риз',
        'Rover': 'Ровер',
        'Saharah': 'Сахара',
        'Snowboy': 'Снеговик',
        'Tom Nook': 'Том Нук',
        'Wardell': 'Уорделл',
        'Wilbur': 'Уилбур',
        'Wisp': 'Дух',
        'Zipper': 'Зиппер',
        # Activities
        'Balloon': 'Шарик',
        'Balloons': 'Шарики',
        'Beach': 'Пляж',
        'Birthday': 'День рождения',
        'Bug catching': 'Ловля насекомых',
        'Cooking': 'Готовка',
        'Crafting': 'Крафт',
        'Diving': 'Дайвинг',
        'Fishing': 'Рыбалка',
        'Mail': 'Почта',
        'Nook Miles Redemption': 'Обмен миль Нука',
        'Nook Shopping': 'Нук Шоппинг',
        'Nook\'s Cranny': 'Лавка Нука',
        'NotAvailable': 'Недоступно',
        'Recycle box': 'Коробка переработки',
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


def _translate_single_source(source: str, lang_sources: Dict[str, str]) -> str:
    """Translate a single source component.
    
    Args:
        source: Single source string (no semicolons)
        lang_sources: Dictionary of translations for the language
    
    Returns:
        Translated source or original if no translation found
    """
    source = source.strip()
    
    # Try exact match first
    if source in lang_sources:
        return lang_sources[source]
    
    # Try case-insensitive match
    source_lower = source.lower()
    for eng_src, translated in lang_sources.items():
        if eng_src.lower() == source_lower:
            return translated
    
    # Handle parenthetical modifiers like "(unlocked after 20 donations)"
    # or "(while stung)" by checking if inner text is translatable
    if source.startswith('(') and source.endswith(')'):
        inner = source[1:-1]
        if inner in lang_sources:
            return f"({lang_sources[inner]})"
        inner_lower = inner.lower()
        for eng_src, translated in lang_sources.items():
            if eng_src.lower() == inner_lower:
                return f"({translated})"
    
    return source


def translate_source(source: str, language: str) -> str:
    """Translate a source name to the user's language.
    
    Handles compound sources separated by semicolons, translating each
    component individually.
    
    Args:
        source: English source name from database (may contain semicolons)
        language: Target language code
    
    Returns:
        Translated source or original if no translation found
    """
    if language == 'en' or not source:
        return source
    
    lang_sources = SOURCE_TRANSLATIONS.get(language, {})
    
    # Handle compound sources (e.g., "Crafting; Nook's Cranny; Franklin")
    if ';' in source:
        parts = source.split(';')
        translated_parts = [_translate_single_source(part, lang_sources) for part in parts]
        return '; '.join(translated_parts)
    
    return _translate_single_source(source, lang_sources)


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
        'result_x_of_n': 'Result {current} of {total}',
        'search_result_for': "for '{query}'",
        'results_range': 'Results {start}-{end}',
        'jump_to_range': 'Jump to range...',
        'select_result': 'Select result...',
        'prev': 'Prev',
        'next': 'Next',
        
        # Type names (singular)
        'type_item': 'Item',
        'type_critter': 'Critter',
        'type_recipe': 'Recipe',
        'type_villager': 'Villager',
        'type_fossil': 'Fossil',
        'type_artwork': 'Artwork',
        
        # Artwork labels
        'genuine': 'Genuine',
        'fake': 'Fake',
        'real_artwork_info': 'Real Artwork Info',
        'artwork_title': 'Title',
        'artwork_artist': 'Artist',
        
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
        'result_x_of_n': '結果 {current}/{total}',
        'search_result_for': "'{query}' の検索",
        'results_range': '結果 {start}-{end}',
        'jump_to_range': '範囲を選択...',
        'select_result': '結果を選択...',
        'prev': '前へ',
        'next': '次へ',
        
        # Type names (singular)
        'type_item': 'アイテム',
        'type_critter': 'いきもの',
        'type_recipe': 'レシピ',
        'type_villager': 'どうぶつ',
        'type_fossil': 'かせき',
        'type_artwork': 'びじゅつひん',
        
        # Artwork labels
        'genuine': 'ほんもの',
        'fake': 'にせもの',
        'real_artwork_info': '本物の美術品情報',
        'artwork_title': 'タイトル',
        'artwork_artist': '作者',
        
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
        'result_x_of_n': '结果 {current}/{total}',
        'search_result_for': "'{query}' 的搜索",
        'results_range': '结果 {start}-{end}',
        'jump_to_range': '跳转到范围...',
        'select_result': '选择结果...',
        'prev': '上一个',
        'next': '下一个',
        
        # Type names (singular)
        'type_item': '物品',
        'type_critter': '生物',
        'type_recipe': '食谱',
        'type_villager': '居民',
        'type_fossil': '化石',
        'type_artwork': '艺术品',
        
        # Artwork labels
        'genuine': '真品',
        'fake': '赝品',
        'real_artwork_info': '真实艺术品信息',
        'artwork_title': '标题',
        'artwork_artist': '艺术家',
        
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
        'result_x_of_n': '결과 {current}/{total}',
        'search_result_for': "'{query}' 검색",
        'results_range': '결과 {start}-{end}',
        'jump_to_range': '범위 선택...',
        'select_result': '결과 선택...',
        'prev': '이전',
        'next': '다음',
        
        # Type names (singular)
        'type_item': '아이템',
        'type_critter': '생물',
        'type_recipe': '레시피',
        'type_villager': '주민',
        'type_fossil': '화석',
        'type_artwork': '미술품',
        
        # Artwork labels
        'genuine': '진품',
        'fake': '위작',
        'real_artwork_info': '실제 미술품 정보',
        'artwork_title': '제목',
        'artwork_artist': '작가',
        
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
        'result_x_of_n': 'Résultat {current} sur {total}',
        'search_result_for': "pour '{query}'",
        'results_range': 'Résultats {start}-{end}',
        'jump_to_range': 'Aller à...',
        'select_result': 'Sélectionner...',
        'prev': 'Préc',
        'next': 'Suiv',
        
        # Type names (singular)
        'type_item': 'Objet',
        'type_critter': 'Créature',
        'type_recipe': 'Recette',
        'type_villager': 'Habitant',
        'type_fossil': 'Fossile',
        'type_artwork': 'Œuvre d\'art',
        
        # Artwork labels
        'genuine': 'Authentique',
        'fake': 'Faux',
        'real_artwork_info': 'Info œuvre réelle',
        'artwork_title': 'Titre',
        'artwork_artist': 'Artiste',
        
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
        'result_x_of_n': 'Ergebnis {current} von {total}',
        'search_result_for': "für '{query}'",
        'results_range': 'Ergebnisse {start}-{end}',
        'jump_to_range': 'Gehe zu...',
        'select_result': 'Auswählen...',
        'prev': 'Zurück',
        'next': 'Weiter',
        
        # Type names (singular)
        'type_item': 'Gegenstand',
        'type_critter': 'Lebewesen',
        'type_recipe': 'Rezept',
        'type_villager': 'Bewohner',
        'type_fossil': 'Fossil',
        'type_artwork': 'Kunstwerk',
        
        # Artwork labels
        'genuine': 'Echt',
        'fake': 'Fälschung',
        'real_artwork_info': 'Infos zum echten Kunstwerk',
        'artwork_title': 'Titel',
        'artwork_artist': 'Künstler',
        
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
        'result_x_of_n': 'Resultado {current} de {total}',
        'search_result_for': "para '{query}'",
        'results_range': 'Resultados {start}-{end}',
        'jump_to_range': 'Ir a...',
        'select_result': 'Seleccionar...',
        'prev': 'Anterior',
        'next': 'Siguiente',
        
        # Type names (singular)
        'type_item': 'Objeto',
        'type_critter': 'Criatura',
        'type_recipe': 'Receta',
        'type_villager': 'Vecino',
        'type_fossil': 'Fósil',
        'type_artwork': 'Obra de arte',
        
        # Artwork labels
        'genuine': 'Auténtico',
        'fake': 'Falso',
        'real_artwork_info': 'Información de la obra real',
        'artwork_title': 'Título',
        'artwork_artist': 'Artista',
        
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
        'result_x_of_n': 'Risultato {current} di {total}',
        'search_result_for': "per '{query}'",
        'results_range': 'Risultati {start}-{end}',
        'jump_to_range': 'Vai a...',
        'select_result': 'Seleziona...',
        'prev': 'Prec',
        'next': 'Succ',
        
        # Type names (singular)
        'type_item': 'Oggetto',
        'type_critter': 'Creatura',
        'type_recipe': 'Ricetta',
        'type_villager': 'Abitante',
        'type_fossil': 'Fossile',
        'type_artwork': 'Opera d\'arte',
        
        # Artwork labels
        'genuine': 'Autentico',
        'fake': 'Falso',
        'real_artwork_info': 'Info opera reale',
        'artwork_title': 'Titolo',
        'artwork_artist': 'Artista',
        
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
        'result_x_of_n': 'Resultaat {current} van {total}',
        'search_result_for': "voor '{query}'",
        'results_range': 'Resultaten {start}-{end}',
        'jump_to_range': 'Ga naar...',
        'select_result': 'Selecteer...',
        'prev': 'Vorige',
        'next': 'Volgende',
        
        # Type names (singular)
        'type_item': 'Voorwerp',
        'type_critter': 'Wezen',
        'type_recipe': 'Recept',
        'type_villager': 'Bewoner',
        'type_fossil': 'Fossiel',
        'type_artwork': 'Kunstwerk',
        
        # Artwork labels
        'genuine': 'Echt',
        'fake': 'Nep',
        'real_artwork_info': 'Informatie echt kunstwerk',
        'artwork_title': 'Titel',
        'artwork_artist': 'Kunstenaar',
        
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
        'result_x_of_n': 'Результат {current} из {total}',
        'search_result_for': "по запросу '{query}'",
        'results_range': 'Результаты {start}-{end}',
        'jump_to_range': 'Перейти к...',
        'select_result': 'Выбрать...',
        'prev': 'Назад',
        'next': 'Далее',
        
        # Type names (singular)
        'type_item': 'Предмет',
        'type_critter': 'Существо',
        'type_recipe': 'Рецепт',
        'type_villager': 'Житель',
        'type_fossil': 'Окаменелость',
        'type_artwork': 'Произведение искусства',
        
        # Artwork labels
        'genuine': 'Подлинник',
        'fake': 'Подделка',
        'real_artwork_info': 'Инфо о настоящем произведении',
        'artwork_title': 'Название',
        'artwork_artist': 'Художник',
        
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
    
    # Search result footer
    def format_result_footer(self, current: int, total: int, query: str) -> str:
        """Format the search result footer text.
        
        Args:
            current: Current result number (1-based)
            total: Total number of results
            query: The search query
        
        Returns:
            Localized footer like "Result 1 of 5 for 'chair'"
        """
        result_part = self._get('result_x_of_n').format(current=current, total=total)
        query_part = self._get('search_result_for').format(query=query)
        return f"{result_part} {query_part}"
    
    def format_single_result_footer(self, query: str) -> str:
        """Format footer for a single search result.
        
        Args:
            query: The search query
        
        Returns:
            Localized footer like "Search result for 'chair'"
        """
        return f"{self._get('search_results')} {self._get('search_result_for').format(query=query)}"
    
    # Navigation buttons
    @property
    def prev_button(self) -> str:
        return self._get('prev')
    
    @property
    def next_button(self) -> str:
        return self._get('next')
    
    # Result selectors
    def format_results_range(self, start: int, end: int) -> str:
        """Format 'Results X-Y' for pagination selector."""
        return self._get('results_range').format(start=start, end=end)
    
    @property
    def jump_to_range(self) -> str:
        return self._get('jump_to_range')
    
    @property
    def select_result(self) -> str:
        return self._get('select_result')
    
    # Type names
    def get_type_name(self, class_name: str) -> str:
        """Get localized type name from Python class name.
        
        Args:
            class_name: Python class name (e.g., 'Item', 'Critter', 'Recipe')
        
        Returns:
            Localized type name
        """
        type_map = {
            'Item': 'type_item',
            'Critter': 'type_critter',
            'Recipe': 'type_recipe',
            'Villager': 'type_villager',
            'Fossil': 'type_fossil',
            'Artwork': 'type_artwork',
        }
        key = type_map.get(class_name, None)
        if key:
            return self._get(key)
        return class_name  # Fallback to original class name
    
    # Artwork labels
    @property
    def genuine(self) -> str:
        return self._get('genuine')
    
    @property
    def fake(self) -> str:
        return self._get('fake')
    
    @property
    def real_artwork_info(self) -> str:
        return self._get('real_artwork_info')
    
    @property
    def artwork_title(self) -> str:
        return self._get('artwork_title')
    
    @property
    def artwork_artist(self) -> str:
        return self._get('artwork_artist')
    
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
