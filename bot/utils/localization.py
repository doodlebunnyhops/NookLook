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


# Fossil details translations (English -> localized)
# These are fossil-specific attributes from the database
FOSSIL_DETAILS_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'en': {
        'No': 'No',
        'Yes': 'Yes',
        'Room 1': 'Room 1',
        'Room 2': 'Room 2',
        'Room 3': 'Room 3',
        'Assessing fossils': 'Assessing fossils',
    },
    'ja': {
        'No': 'なし',
        'Yes': 'あり',
        'Room 1': '部屋1',
        'Room 2': '部屋2',
        'Room 3': '部屋3',
        'Assessing fossils': 'かせきのかんてい',
    },
    'zh': {
        'No': '否',
        'Yes': '是',
        'Room 1': '房间1',
        'Room 2': '房间2',
        'Room 3': '房间3',
        'Assessing fossils': '鉴定化石',
    },
    'ko': {
        'No': '아니오',
        'Yes': '예',
        'Room 1': '방 1',
        'Room 2': '방 2',
        'Room 3': '방 3',
        'Assessing fossils': '화석 감정',
    },
    'fr': {
        'No': 'Non',
        'Yes': 'Oui',
        'Room 1': 'Salle 1',
        'Room 2': 'Salle 2',
        'Room 3': 'Salle 3',
        'Assessing fossils': 'Évaluation des fossiles',
    },
    'de': {
        'No': 'Nein',
        'Yes': 'Ja',
        'Room 1': 'Raum 1',
        'Room 2': 'Raum 2',
        'Room 3': 'Raum 3',
        'Assessing fossils': 'Fossilien bewerten',
    },
    'es': {
        'No': 'No',
        'Yes': 'Sí',
        'Room 1': 'Sala 1',
        'Room 2': 'Sala 2',
        'Room 3': 'Sala 3',
        'Assessing fossils': 'Evaluando fósiles',
    },
    'it': {
        'No': 'No',
        'Yes': 'Sì',
        'Room 1': 'Sala 1',
        'Room 2': 'Sala 2',
        'Room 3': 'Sala 3',
        'Assessing fossils': 'Valutazione fossili',
    },
    'nl': {
        'No': 'Nee',
        'Yes': 'Ja',
        'Room 1': 'Kamer 1',
        'Room 2': 'Kamer 2',
        'Room 3': 'Kamer 3',
        'Assessing fossils': 'Fossielen beoordelen',
    },
    'ru': {
        'No': 'Нет',
        'Yes': 'Да',
        'Room 1': 'Комната 1',
        'Room 2': 'Комната 2',
        'Room 3': 'Комната 3',
        'Assessing fossils': 'Оценка окаменелостей',
    },
}


# Villager details translations (English -> localized)
# These are villager-specific attributes from the database
VILLAGER_DETAILS_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'ja': {
        # Species
        'Alligator': 'ワニ',
        'Anteater': 'アリクイ',
        'Bear': 'クマ',
        'Bear cub': 'コグマ',
        'Bird': 'トリ',
        'Bull': 'ウシ',
        'Cat': 'ネコ',
        'Chicken': 'ニワトリ',
        'Cow': 'ウシ',
        'Deer': 'シカ',
        'Dog': 'イヌ',
        'Duck': 'アヒル',
        'Eagle': 'ワシ',
        'Elephant': 'ゾウ',
        'Frog': 'カエル',
        'Goat': 'ヤギ',
        'Gorilla': 'ゴリラ',
        'Hamster': 'ハムスター',
        'Hippo': 'カバ',
        'Horse': 'ウマ',
        'Kangaroo': 'カンガルー',
        'Koala': 'コアラ',
        'Lion': 'ライオン',
        'Monkey': 'サル',
        'Mouse': 'ネズミ',
        'Octopus': 'タコ',
        'Ostrich': 'ダチョウ',
        'Penguin': 'ペンギン',
        'Pig': 'ブタ',
        'Rabbit': 'ウサギ',
        'Rhinoceros': 'サイ',
        'Sheep': 'ヒツジ',
        'Squirrel': 'リス',
        'Tiger': 'トラ',
        'Wolf': 'オオカミ',
        # Personality
        'Big Sister': 'アネキ',
        'Cranky': 'コワイ',
        'Jock': 'ハキハキ',
        'Lazy': 'ボンヤリ',
        'Normal': 'フツウ',
        'Peppy': 'ゲンキ',
        'Smug': 'キザ',
        'Snooty': 'オトナ',
        # Hobby
        'Nature': 'しぜん',
        'Fitness': 'フィットネス',
        'Play': 'あそび',
        'Education': 'べんきょう',
        'Fashion': 'ファッション',
        'Music': 'おんがく',
        # Style
        'Active': 'アクティブ',
        'Cool': 'クール',
        'Simple': 'シンプル',
        'Cute': 'キュート',
        'Gorgeous': 'ゴージャス',
        'Elegant': 'エレガント',
        # Color
        'Aqua': 'アクア',
        'Beige': 'ベージュ',
        'Black': 'ブラック',
        'Blue': 'ブルー',
        'Brown': 'ブラウン',
        'Colorful': 'カラフル',
        'Gray': 'グレー',
        'Green': 'グリーン',
        'Orange': 'オレンジ',
        'Pink': 'ピンク',
        'Purple': 'パープル',
        'Red': 'レッド',
        'White': 'ホワイト',
        'Yellow': 'イエロー',
    },
    'zh': {
        # Species
        'Alligator': '鳄鱼',
        'Anteater': '食蚁兽',
        'Bear': '熊',
        'Bear cub': '小熊',
        'Bird': '鸟',
        'Bull': '公牛',
        'Cat': '猫',
        'Chicken': '鸡',
        'Cow': '牛',
        'Deer': '鹿',
        'Dog': '狗',
        'Duck': '鸭',
        'Eagle': '鹰',
        'Elephant': '象',
        'Frog': '青蛙',
        'Goat': '山羊',
        'Gorilla': '猩猩',
        'Hamster': '仓鼠',
        'Hippo': '河马',
        'Horse': '马',
        'Kangaroo': '袋鼠',
        'Koala': '考拉',
        'Lion': '狮子',
        'Monkey': '猴子',
        'Mouse': '老鼠',
        'Octopus': '章鱼',
        'Ostrich': '鸵鸟',
        'Penguin': '企鹅',
        'Pig': '猪',
        'Rabbit': '兔子',
        'Rhinoceros': '犀牛',
        'Sheep': '绵羊',
        'Squirrel': '松鼠',
        'Tiger': '老虎',
        'Wolf': '狼',
        # Personality
        'Big Sister': '大姐姐',
        'Cranky': '暴躁',
        'Jock': '运动',
        'Lazy': '悠闲',
        'Normal': '普通',
        'Peppy': '元气',
        'Smug': '自恋',
        'Snooty': '成熟',
        # Hobby
        'Nature': '自然',
        'Fitness': '健身',
        'Play': '玩耍',
        'Education': '学习',
        'Fashion': '时尚',
        'Music': '音乐',
        # Style
        'Active': '活力',
        'Cool': '酷',
        'Simple': '简单',
        'Cute': '可爱',
        'Gorgeous': '华丽',
        'Elegant': '优雅',
        # Color
        'Aqua': '水色',
        'Beige': '米色',
        'Black': '黑色',
        'Blue': '蓝色',
        'Brown': '棕色',
        'Colorful': '彩色',
        'Gray': '灰色',
        'Green': '绿色',
        'Orange': '橙色',
        'Pink': '粉色',
        'Purple': '紫色',
        'Red': '红色',
        'White': '白色',
        'Yellow': '黄色',
    },
    'ko': {
        # Species
        'Alligator': '악어',
        'Anteater': '개미핥기',
        'Bear': '곰',
        'Bear cub': '아기곰',
        'Bird': '새',
        'Bull': '황소',
        'Cat': '고양이',
        'Chicken': '닭',
        'Cow': '소',
        'Deer': '사슴',
        'Dog': '개',
        'Duck': '오리',
        'Eagle': '독수리',
        'Elephant': '코끼리',
        'Frog': '개구리',
        'Goat': '염소',
        'Gorilla': '고릴라',
        'Hamster': '햄스터',
        'Hippo': '하마',
        'Horse': '말',
        'Kangaroo': '캥거루',
        'Koala': '코알라',
        'Lion': '사자',
        'Monkey': '원숭이',
        'Mouse': '쥐',
        'Octopus': '문어',
        'Ostrich': '타조',
        'Penguin': '펭귄',
        'Pig': '돼지',
        'Rabbit': '토끼',
        'Rhinoceros': '코뿔소',
        'Sheep': '양',
        'Squirrel': '다람쥐',
        'Tiger': '호랑이',
        'Wolf': '늑대',
        # Personality
        'Big Sister': '단순활발',
        'Cranky': '무뚝뚝',
        'Jock': '운동광',
        'Lazy': '먹보',
        'Normal': '친절함',
        'Peppy': '아이돌',
        'Smug': '느끼함',
        'Snooty': '성숙함',
        # Hobby
        'Nature': '자연',
        'Fitness': '운동',
        'Play': '놀이',
        'Education': '공부',
        'Fashion': '패션',
        'Music': '음악',
        # Style
        'Active': '액티브',
        'Cool': '쿨',
        'Simple': '심플',
        'Cute': '큐트',
        'Gorgeous': '고저스',
        'Elegant': '엘레강스',
        # Color
        'Aqua': '아쿠아',
        'Beige': '베이지',
        'Black': '블랙',
        'Blue': '블루',
        'Brown': '브라운',
        'Colorful': '컬러풀',
        'Gray': '그레이',
        'Green': '그린',
        'Orange': '오렌지',
        'Pink': '핑크',
        'Purple': '퍼플',
        'Red': '레드',
        'White': '화이트',
        'Yellow': '옐로',
    },
    'fr': {
        # Species
        'Alligator': 'Alligator',
        'Anteater': 'Tamanoir',
        'Bear': 'Ours',
        'Bear cub': 'Ourson',
        'Bird': 'Oiseau',
        'Bull': 'Taureau',
        'Cat': 'Chat',
        'Chicken': 'Poule',
        'Cow': 'Vache',
        'Deer': 'Cerf',
        'Dog': 'Chien',
        'Duck': 'Canard',
        'Eagle': 'Aigle',
        'Elephant': 'Éléphant',
        'Frog': 'Grenouille',
        'Goat': 'Chèvre',
        'Gorilla': 'Gorille',
        'Hamster': 'Hamster',
        'Hippo': 'Hippopotame',
        'Horse': 'Cheval',
        'Kangaroo': 'Kangourou',
        'Koala': 'Koala',
        'Lion': 'Lion',
        'Monkey': 'Singe',
        'Mouse': 'Souris',
        'Octopus': 'Pieuvre',
        'Ostrich': 'Autruche',
        'Penguin': 'Pingouin',
        'Pig': 'Cochon',
        'Rabbit': 'Lapin',
        'Rhinoceros': 'Rhinocéros',
        'Sheep': 'Mouton',
        'Squirrel': 'Écureuil',
        'Tiger': 'Tigre',
        'Wolf': 'Loup',
        # Personality
        'Big Sister': 'Grande sœur',
        'Cranky': 'Grognon',
        'Jock': 'Sportif',
        'Lazy': 'Paresseux',
        'Normal': 'Normale',
        'Peppy': 'Pétillante',
        'Smug': 'Suffisant',
        'Snooty': 'Snob',
        # Hobby
        'Nature': 'Nature',
        'Fitness': 'Fitness',
        'Play': 'Jeu',
        'Education': 'Éducation',
        'Fashion': 'Mode',
        'Music': 'Musique',
        # Style
        'Active': 'Actif',
        'Cool': 'Cool',
        'Simple': 'Simple',
        'Cute': 'Mignon',
        'Gorgeous': 'Magnifique',
        'Elegant': 'Élégant',
        # Color
        'Aqua': 'Turquoise',
        'Beige': 'Beige',
        'Black': 'Noir',
        'Blue': 'Bleu',
        'Brown': 'Marron',
        'Colorful': 'Coloré',
        'Gray': 'Gris',
        'Green': 'Vert',
        'Orange': 'Orange',
        'Pink': 'Rose',
        'Purple': 'Violet',
        'Red': 'Rouge',
        'White': 'Blanc',
        'Yellow': 'Jaune',
    },
    'de': {
        # Species
        'Alligator': 'Alligator',
        'Anteater': 'Ameisenbär',
        'Bear': 'Bär',
        'Bear cub': 'Bärenjunges',
        'Bird': 'Vogel',
        'Bull': 'Stier',
        'Cat': 'Katze',
        'Chicken': 'Huhn',
        'Cow': 'Kuh',
        'Deer': 'Hirsch',
        'Dog': 'Hund',
        'Duck': 'Ente',
        'Eagle': 'Adler',
        'Elephant': 'Elefant',
        'Frog': 'Frosch',
        'Goat': 'Ziege',
        'Gorilla': 'Gorilla',
        'Hamster': 'Hamster',
        'Hippo': 'Nilpferd',
        'Horse': 'Pferd',
        'Kangaroo': 'Känguru',
        'Koala': 'Koala',
        'Lion': 'Löwe',
        'Monkey': 'Affe',
        'Mouse': 'Maus',
        'Octopus': 'Oktopus',
        'Ostrich': 'Strauß',
        'Penguin': 'Pinguin',
        'Pig': 'Schwein',
        'Rabbit': 'Hase',
        'Rhinoceros': 'Nashorn',
        'Sheep': 'Schaf',
        'Squirrel': 'Eichhörnchen',
        'Tiger': 'Tiger',
        'Wolf': 'Wolf',
        # Personality
        'Big Sister': 'Große Schwester',
        'Cranky': 'Miesepeter',
        'Jock': 'Sportlich',
        'Lazy': 'Faul',
        'Normal': 'Normal',
        'Peppy': 'Fröhlich',
        'Smug': 'Eingebildet',
        'Snooty': 'Hochnäsig',
        # Hobby
        'Nature': 'Natur',
        'Fitness': 'Fitness',
        'Play': 'Spielen',
        'Education': 'Bildung',
        'Fashion': 'Mode',
        'Music': 'Musik',
        # Style
        'Active': 'Aktiv',
        'Cool': 'Cool',
        'Simple': 'Einfach',
        'Cute': 'Süß',
        'Gorgeous': 'Prächtig',
        'Elegant': 'Elegant',
        # Color
        'Aqua': 'Aqua',
        'Beige': 'Beige',
        'Black': 'Schwarz',
        'Blue': 'Blau',
        'Brown': 'Braun',
        'Colorful': 'Bunt',
        'Gray': 'Grau',
        'Green': 'Grün',
        'Orange': 'Orange',
        'Pink': 'Rosa',
        'Purple': 'Lila',
        'Red': 'Rot',
        'White': 'Weiß',
        'Yellow': 'Gelb',
    },
    'es': {
        # Species
        'Alligator': 'Caimán',
        'Anteater': 'Oso hormiguero',
        'Bear': 'Oso',
        'Bear cub': 'Osito',
        'Bird': 'Pájaro',
        'Bull': 'Toro',
        'Cat': 'Gato',
        'Chicken': 'Gallina',
        'Cow': 'Vaca',
        'Deer': 'Ciervo',
        'Dog': 'Perro',
        'Duck': 'Pato',
        'Eagle': 'Águila',
        'Elephant': 'Elefante',
        'Frog': 'Rana',
        'Goat': 'Cabra',
        'Gorilla': 'Gorila',
        'Hamster': 'Hámster',
        'Hippo': 'Hipopótamo',
        'Horse': 'Caballo',
        'Kangaroo': 'Canguro',
        'Koala': 'Koala',
        'Lion': 'León',
        'Monkey': 'Mono',
        'Mouse': 'Ratón',
        'Octopus': 'Pulpo',
        'Ostrich': 'Avestruz',
        'Penguin': 'Pingüino',
        'Pig': 'Cerdo',
        'Rabbit': 'Conejo',
        'Rhinoceros': 'Rinoceronte',
        'Sheep': 'Oveja',
        'Squirrel': 'Ardilla',
        'Tiger': 'Tigre',
        'Wolf': 'Lobo',
        # Personality
        'Big Sister': 'Hermana mayor',
        'Cranky': 'Gruñón',
        'Jock': 'Atlético',
        'Lazy': 'Perezoso',
        'Normal': 'Normal',
        'Peppy': 'Alegre',
        'Smug': 'Presumido',
        'Snooty': 'Esnob',
        # Hobby
        'Nature': 'Naturaleza',
        'Fitness': 'Ejercicio',
        'Play': 'Jugar',
        'Education': 'Educación',
        'Fashion': 'Moda',
        'Music': 'Música',
        # Style
        'Active': 'Activo',
        'Cool': 'Genial',
        'Simple': 'Simple',
        'Cute': 'Mono',
        'Gorgeous': 'Fabuloso',
        'Elegant': 'Elegante',
        # Color
        'Aqua': 'Aguamarina',
        'Beige': 'Beige',
        'Black': 'Negro',
        'Blue': 'Azul',
        'Brown': 'Marrón',
        'Colorful': 'Colorido',
        'Gray': 'Gris',
        'Green': 'Verde',
        'Orange': 'Naranja',
        'Pink': 'Rosa',
        'Purple': 'Morado',
        'Red': 'Rojo',
        'White': 'Blanco',
        'Yellow': 'Amarillo',
    },
    'it': {
        # Species
        'Alligator': 'Alligatore',
        'Anteater': 'Formichiere',
        'Bear': 'Orso',
        'Bear cub': 'Orsetto',
        'Bird': 'Uccello',
        'Bull': 'Toro',
        'Cat': 'Gatto',
        'Chicken': 'Gallina',
        'Cow': 'Mucca',
        'Deer': 'Cervo',
        'Dog': 'Cane',
        'Duck': 'Anatra',
        'Eagle': 'Aquila',
        'Elephant': 'Elefante',
        'Frog': 'Rana',
        'Goat': 'Capra',
        'Gorilla': 'Gorilla',
        'Hamster': 'Criceto',
        'Hippo': 'Ippopotamo',
        'Horse': 'Cavallo',
        'Kangaroo': 'Canguro',
        'Koala': 'Koala',
        'Lion': 'Leone',
        'Monkey': 'Scimmia',
        'Mouse': 'Topo',
        'Octopus': 'Polpo',
        'Ostrich': 'Struzzo',
        'Penguin': 'Pinguino',
        'Pig': 'Maiale',
        'Rabbit': 'Coniglio',
        'Rhinoceros': 'Rinoceronte',
        'Sheep': 'Pecora',
        'Squirrel': 'Scoiattolo',
        'Tiger': 'Tigre',
        'Wolf': 'Lupo',
        # Personality
        'Big Sister': 'Sorella maggiore',
        'Cranky': 'Burbero',
        'Jock': 'Sportivo',
        'Lazy': 'Pigro',
        'Normal': 'Normale',
        'Peppy': 'Vivace',
        'Smug': 'Vanitoso',
        'Snooty': 'Snob',
        # Hobby
        'Nature': 'Natura',
        'Fitness': 'Fitness',
        'Play': 'Gioco',
        'Education': 'Istruzione',
        'Fashion': 'Moda',
        'Music': 'Musica',
        # Style
        'Active': 'Attivo',
        'Cool': 'Figo',
        'Simple': 'Semplice',
        'Cute': 'Carino',
        'Gorgeous': 'Splendido',
        'Elegant': 'Elegante',
        # Color
        'Aqua': 'Acqua',
        'Beige': 'Beige',
        'Black': 'Nero',
        'Blue': 'Blu',
        'Brown': 'Marrone',
        'Colorful': 'Colorato',
        'Gray': 'Grigio',
        'Green': 'Verde',
        'Orange': 'Arancione',
        'Pink': 'Rosa',
        'Purple': 'Viola',
        'Red': 'Rosso',
        'White': 'Bianco',
        'Yellow': 'Giallo',
    },
    'nl': {
        # Species
        'Alligator': 'Alligator',
        'Anteater': 'Miereneter',
        'Bear': 'Beer',
        'Bear cub': 'Berenwelp',
        'Bird': 'Vogel',
        'Bull': 'Stier',
        'Cat': 'Kat',
        'Chicken': 'Kip',
        'Cow': 'Koe',
        'Deer': 'Hert',
        'Dog': 'Hond',
        'Duck': 'Eend',
        'Eagle': 'Arend',
        'Elephant': 'Olifant',
        'Frog': 'Kikker',
        'Goat': 'Geit',
        'Gorilla': 'Gorilla',
        'Hamster': 'Hamster',
        'Hippo': 'Nijlpaard',
        'Horse': 'Paard',
        'Kangaroo': 'Kangoeroe',
        'Koala': 'Koala',
        'Lion': 'Leeuw',
        'Monkey': 'Aap',
        'Mouse': 'Muis',
        'Octopus': 'Octopus',
        'Ostrich': 'Struisvogel',
        'Penguin': 'Pinguïn',
        'Pig': 'Varken',
        'Rabbit': 'Konijn',
        'Rhinoceros': 'Neushoorn',
        'Sheep': 'Schaap',
        'Squirrel': 'Eekhoorn',
        'Tiger': 'Tijger',
        'Wolf': 'Wolf',
        # Personality
        'Big Sister': 'Grote zus',
        'Cranky': 'Chagrijnig',
        'Jock': 'Sportief',
        'Lazy': 'Lui',
        'Normal': 'Normaal',
        'Peppy': 'Vrolijk',
        'Smug': 'Zelfingenomen',
        'Snooty': 'Verwaand',
        # Hobby
        'Nature': 'Natuur',
        'Fitness': 'Fitness',
        'Play': 'Spelen',
        'Education': 'Onderwijs',
        'Fashion': 'Mode',
        'Music': 'Muziek',
        # Style
        'Active': 'Actief',
        'Cool': 'Cool',
        'Simple': 'Eenvoudig',
        'Cute': 'Schattig',
        'Gorgeous': 'Prachtig',
        'Elegant': 'Elegant',
        # Color
        'Aqua': 'Aqua',
        'Beige': 'Beige',
        'Black': 'Zwart',
        'Blue': 'Blauw',
        'Brown': 'Bruin',
        'Colorful': 'Kleurrijk',
        'Gray': 'Grijs',
        'Green': 'Groen',
        'Orange': 'Oranje',
        'Pink': 'Roze',
        'Purple': 'Paars',
        'Red': 'Rood',
        'White': 'Wit',
        'Yellow': 'Geel',
    },
    'ru': {
        # Species
        'Alligator': 'Аллигатор',
        'Anteater': 'Муравьед',
        'Bear': 'Медведь',
        'Bear cub': 'Медвежонок',
        'Bird': 'Птица',
        'Bull': 'Бык',
        'Cat': 'Кошка',
        'Chicken': 'Курица',
        'Cow': 'Корова',
        'Deer': 'Олень',
        'Dog': 'Собака',
        'Duck': 'Утка',
        'Eagle': 'Орёл',
        'Elephant': 'Слон',
        'Frog': 'Лягушка',
        'Goat': 'Коза',
        'Gorilla': 'Горилла',
        'Hamster': 'Хомяк',
        'Hippo': 'Бегемот',
        'Horse': 'Лошадь',
        'Kangaroo': 'Кенгуру',
        'Koala': 'Коала',
        'Lion': 'Лев',
        'Monkey': 'Обезьяна',
        'Mouse': 'Мышь',
        'Octopus': 'Осьминог',
        'Ostrich': 'Страус',
        'Penguin': 'Пингвин',
        'Pig': 'Свинья',
        'Rabbit': 'Кролик',
        'Rhinoceros': 'Носорог',
        'Sheep': 'Овца',
        'Squirrel': 'Белка',
        'Tiger': 'Тигр',
        'Wolf': 'Волк',
        # Personality
        'Big Sister': 'Старшая сестра',
        'Cranky': 'Ворчун',
        'Jock': 'Спортсмен',
        'Lazy': 'Лентяй',
        'Normal': 'Обычный',
        'Peppy': 'Задорный',
        'Smug': 'Самодовольный',
        'Snooty': 'Высокомерный',
        # Hobby
        'Nature': 'Природа',
        'Fitness': 'Фитнес',
        'Play': 'Игры',
        'Education': 'Образование',
        'Fashion': 'Мода',
        'Music': 'Музыка',
        # Style
        'Active': 'Активный',
        'Cool': 'Крутой',
        'Simple': 'Простой',
        'Cute': 'Милый',
        'Gorgeous': 'Шикарный',
        'Elegant': 'Элегантный',
        # Color
        'Aqua': 'Аква',
        'Beige': 'Бежевый',
        'Black': 'Чёрный',
        'Blue': 'Синий',
        'Brown': 'Коричневый',
        'Colorful': 'Разноцветный',
        'Gray': 'Серый',
        'Green': 'Зелёный',
        'Orange': 'Оранжевый',
        'Pink': 'Розовый',
        'Purple': 'Фиолетовый',
        'Red': 'Красный',
        'White': 'Белый',
        'Yellow': 'Жёлтый',
    },
}


# Critter details translations (English -> localized)
# These are critter-specific attributes from the database
CRITTER_DETAILS_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'ja': {
        # Location
        'Disguised on shoreline': '海岸に擬態',
        'Disguised under trees': '木の下に擬態',
        'Flying': '飛んでいる',
        'Flying near blue/purple/black flowers': '青/紫/黒の花の近くを飛んでいる',
        'Flying near flowers': '花の近くを飛んでいる',
        'Flying near light sources': '光源の近くを飛んでいる',
        'Flying near trash (boots, tires, cans, used fountain fireworks) or rotten turnips': 'ゴミ（長靴、タイヤ、空き缶、使用済み噴水花火）や腐ったカブの近くを飛んでいる',
        'Flying near water': '水辺を飛んでいる',
        'From hitting rocks': '岩を叩いて出現',
        'On beach rocks': '浜辺の岩の上',
        'On flowers': '花の上',
        'On hardwood/cedar trees': '広葉樹/針葉樹の上',
        'On palm trees': 'ヤシの木の上',
        'On rivers/ponds': '川/池の上',
        'On rocks/bushes': '岩/低木の上',
        'On rotten turnips or candy': '腐ったカブやアメの上',
        'On the ground': '地面の上',
        'On tree stumps': '切り株の上',
        'On trees (any kind)': '木の上（種類問わず）',
        'On villagers': '住民の上',
        'On white flowers': '白い花の上',
        'Pier': '桟橋',
        'Pond': '池',
        'Pushing snowballs': '雪玉を転がしている',
        'River': '川',
        'River (clifftop)': '川（崖の上）',
        'River (mouth)': '河口',
        'Sea': '海',
        'Sea (rainy days)': '海（雨の日）',
        'Shaking trees': '木を揺らして出現',
        'Shaking trees (hardwood or cedar only)': '木を揺らして出現（広葉樹または針葉樹のみ）',
        'Underground (dig where noise is loudest)': '地中（音が一番大きい場所を掘る）',
        # Time
        'All day': '終日',
        'All Day': '終日',
        # Weather
        'Any except rain': '雨以外',
        'Any weather': 'どんな天気でも',
        'Rain only': '雨の日のみ',
        # Shadow Size
        'Large': '大',
        'Long': '細長',
        'Medium': '中',
        'Small': '小',
        'X-Large': '特大',
        'X-Large w/Fin': '特大（ヒレ付き）',
        'X-Small': '極小',
        'XX-Large': '超特大',
        # Catch Difficulty
        'Easy': 'かんたん',
        'Hard': 'むずかしい',
        'Very Easy': 'とてもかんたん',
        'Very Hard': 'とてもむずかしい',
        # Vision
        'Narrow': '狭い',
        'Very Narrow': 'とても狭い',
        'Very Wide': 'とても広い',
        'Wide': '広い',
        # Movement
        'Fast': '速い',
        'Slow': '遅い',
        'Stationary': '静止',
        'Very fast': 'とても速い',
        'Very slow': 'とても遅い',
    },
    'zh': {
        # Location
        'Disguised on shoreline': '伪装在海岸线上',
        'Disguised under trees': '伪装在树下',
        'Flying': '飞行中',
        'Flying near blue/purple/black flowers': '在蓝/紫/黑色花朵附近飞行',
        'Flying near flowers': '在花朵附近飞行',
        'Flying near light sources': '在光源附近飞行',
        'Flying near trash (boots, tires, cans, used fountain fireworks) or rotten turnips': '在垃圾（靴子、轮胎、罐子、用过的烟花）或烂萝卜附近飞行',
        'Flying near water': '在水边飞行',
        'From hitting rocks': '敲击岩石出现',
        'On beach rocks': '在海滩岩石上',
        'On flowers': '在花朵上',
        'On hardwood/cedar trees': '在阔叶树/雪松树上',
        'On palm trees': '在棕榈树上',
        'On rivers/ponds': '在河流/池塘上',
        'On rocks/bushes': '在岩石/灌木上',
        'On rotten turnips or candy': '在烂萝卜或糖果上',
        'On the ground': '在地面上',
        'On tree stumps': '在树桩上',
        'On trees (any kind)': '在树上（任何类型）',
        'On villagers': '在村民身上',
        'On white flowers': '在白花上',
        'Pier': '码头',
        'Pond': '池塘',
        'Pushing snowballs': '推雪球',
        'River': '河流',
        'River (clifftop)': '河流（悬崖顶）',
        'River (mouth)': '河口',
        'Sea': '大海',
        'Sea (rainy days)': '大海（雨天）',
        'Shaking trees': '摇晃树木出现',
        'Shaking trees (hardwood or cedar only)': '摇晃树木出现（仅阔叶树或雪松）',
        'Underground (dig where noise is loudest)': '地下（在声音最大的地方挖掘）',
        # Time
        'All day': '全天',
        'All Day': '全天',
        # Weather
        'Any except rain': '除雨天外',
        'Any weather': '任何天气',
        'Rain only': '仅雨天',
        # Shadow Size
        'Large': '大',
        'Long': '细长',
        'Medium': '中',
        'Small': '小',
        'X-Large': '特大',
        'X-Large w/Fin': '特大（带鳍）',
        'X-Small': '特小',
        'XX-Large': '超特大',
        # Catch Difficulty
        'Easy': '简单',
        'Hard': '困难',
        'Very Easy': '非常简单',
        'Very Hard': '非常困难',
        # Vision
        'Narrow': '窄',
        'Very Narrow': '非常窄',
        'Very Wide': '非常宽',
        'Wide': '宽',
        # Movement
        'Fast': '快',
        'Slow': '慢',
        'Stationary': '静止',
        'Very fast': '非常快',
        'Very slow': '非常慢',
    },
    'ko': {
        # Location
        'Disguised on shoreline': '해안선에 위장',
        'Disguised under trees': '나무 아래에 위장',
        'Flying': '비행 중',
        'Flying near blue/purple/black flowers': '파란/보라/검은 꽃 근처를 비행',
        'Flying near flowers': '꽃 근처를 비행',
        'Flying near light sources': '광원 근처를 비행',
        'Flying near trash (boots, tires, cans, used fountain fireworks) or rotten turnips': '쓰레기(장화, 타이어, 캔, 사용한 분수 불꽃놀이) 또는 썩은 순무 근처를 비행',
        'Flying near water': '물가를 비행',
        'From hitting rocks': '바위를 쳐서 출현',
        'On beach rocks': '해변 바위 위',
        'On flowers': '꽃 위',
        'On hardwood/cedar trees': '활엽수/삼나무 위',
        'On palm trees': '야자수 위',
        'On rivers/ponds': '강/연못 위',
        'On rocks/bushes': '바위/덤불 위',
        'On rotten turnips or candy': '썩은 순무 또는 사탕 위',
        'On the ground': '땅 위',
        'On tree stumps': '그루터기 위',
        'On trees (any kind)': '나무 위 (모든 종류)',
        'On villagers': '주민 위',
        'On white flowers': '흰 꽃 위',
        'Pier': '부두',
        'Pond': '연못',
        'Pushing snowballs': '눈덩이 굴리기',
        'River': '강',
        'River (clifftop)': '강 (절벽 위)',
        'River (mouth)': '하구',
        'Sea': '바다',
        'Sea (rainy days)': '바다 (비 오는 날)',
        'Shaking trees': '나무 흔들어 출현',
        'Shaking trees (hardwood or cedar only)': '나무 흔들어 출현 (활엽수 또는 삼나무만)',
        'Underground (dig where noise is loudest)': '지하 (소리가 가장 큰 곳을 파세요)',
        # Time
        'All day': '하루 종일',
        'All Day': '하루 종일',
        # Weather
        'Any except rain': '비 제외',
        'Any weather': '모든 날씨',
        'Rain only': '비 오는 날만',
        # Shadow Size
        'Large': '대형',
        'Long': '길쭉',
        'Medium': '중형',
        'Small': '소형',
        'X-Large': '특대형',
        'X-Large w/Fin': '특대형 (지느러미)',
        'X-Small': '극소형',
        'XX-Large': '초특대형',
        # Catch Difficulty
        'Easy': '쉬움',
        'Hard': '어려움',
        'Very Easy': '매우 쉬움',
        'Very Hard': '매우 어려움',
        # Vision
        'Narrow': '좁음',
        'Very Narrow': '매우 좁음',
        'Very Wide': '매우 넓음',
        'Wide': '넓음',
        # Movement
        'Fast': '빠름',
        'Slow': '느림',
        'Stationary': '정지',
        'Very fast': '매우 빠름',
        'Very slow': '매우 느림',
    },
    'fr': {
        # Location
        'Disguised on shoreline': 'Camouflé sur le rivage',
        'Disguised under trees': 'Camouflé sous les arbres',
        'Flying': 'En vol',
        'Flying near blue/purple/black flowers': 'Vole près des fleurs bleues/violettes/noires',
        'Flying near flowers': 'Vole près des fleurs',
        'Flying near light sources': 'Vole près des sources de lumière',
        'Flying near trash (boots, tires, cans, used fountain fireworks) or rotten turnips': 'Vole près des déchets (bottes, pneus, canettes, feux d\'artifice usagés) ou navets pourris',
        'Flying near water': 'Vole près de l\'eau',
        'From hitting rocks': 'En frappant les rochers',
        'On beach rocks': 'Sur les rochers de plage',
        'On flowers': 'Sur les fleurs',
        'On hardwood/cedar trees': 'Sur les feuillus/cèdres',
        'On palm trees': 'Sur les palmiers',
        'On rivers/ponds': 'Sur les rivières/étangs',
        'On rocks/bushes': 'Sur les rochers/buissons',
        'On rotten turnips or candy': 'Sur les navets pourris ou bonbons',
        'On the ground': 'Au sol',
        'On tree stumps': 'Sur les souches',
        'On trees (any kind)': 'Sur les arbres (tout type)',
        'On villagers': 'Sur les villageois',
        'On white flowers': 'Sur les fleurs blanches',
        'Pier': 'Ponton',
        'Pond': 'Étang',
        'Pushing snowballs': 'En poussant des boules de neige',
        'River': 'Rivière',
        'River (clifftop)': 'Rivière (falaise)',
        'River (mouth)': 'Embouchure',
        'Sea': 'Mer',
        'Sea (rainy days)': 'Mer (jours de pluie)',
        'Shaking trees': 'En secouant les arbres',
        'Shaking trees (hardwood or cedar only)': 'En secouant les arbres (feuillus ou cèdres uniquement)',
        'Underground (dig where noise is loudest)': 'Souterrain (creusez où le bruit est le plus fort)',
        # Time
        'All day': 'Toute la journée',
        'All Day': 'Toute la journée',
        # Weather
        'Any except rain': 'Tout sauf la pluie',
        'Any weather': 'Tout temps',
        'Rain only': 'Pluie uniquement',
        # Shadow Size
        'Large': 'Grand',
        'Long': 'Long',
        'Medium': 'Moyen',
        'Small': 'Petit',
        'X-Large': 'Très grand',
        'X-Large w/Fin': 'Très grand avec aileron',
        'X-Small': 'Très petit',
        'XX-Large': 'Énorme',
        # Catch Difficulty
        'Easy': 'Facile',
        'Hard': 'Difficile',
        'Very Easy': 'Très facile',
        'Very Hard': 'Très difficile',
        # Vision
        'Narrow': 'Étroit',
        'Very Narrow': 'Très étroit',
        'Very Wide': 'Très large',
        'Wide': 'Large',
        # Movement
        'Fast': 'Rapide',
        'Slow': 'Lent',
        'Stationary': 'Immobile',
        'Very fast': 'Très rapide',
        'Very slow': 'Très lent',
    },
    'de': {
        # Location
        'Disguised on shoreline': 'Getarnt am Ufer',
        'Disguised under trees': 'Getarnt unter Bäumen',
        'Flying': 'Fliegend',
        'Flying near blue/purple/black flowers': 'Fliegt bei blauen/lila/schwarzen Blumen',
        'Flying near flowers': 'Fliegt bei Blumen',
        'Flying near light sources': 'Fliegt bei Lichtquellen',
        'Flying near trash (boots, tires, cans, used fountain fireworks) or rotten turnips': 'Fliegt bei Müll (Stiefel, Reifen, Dosen, Springbrunnen-Feuerwerk) oder faulen Rüben',
        'Flying near water': 'Fliegt am Wasser',
        'From hitting rocks': 'Beim Steineklopfen',
        'On beach rocks': 'Auf Strandfelsen',
        'On flowers': 'Auf Blumen',
        'On hardwood/cedar trees': 'Auf Laub-/Nadelbäumen',
        'On palm trees': 'Auf Palmen',
        'On rivers/ponds': 'Auf Flüssen/Teichen',
        'On rocks/bushes': 'Auf Steinen/Büschen',
        'On rotten turnips or candy': 'Auf faulen Rüben oder Süßigkeiten',
        'On the ground': 'Auf dem Boden',
        'On tree stumps': 'Auf Baumstümpfen',
        'On trees (any kind)': 'Auf Bäumen (jede Art)',
        'On villagers': 'Auf Bewohnern',
        'On white flowers': 'Auf weißen Blumen',
        'Pier': 'Steg',
        'Pond': 'Teich',
        'Pushing snowballs': 'Beim Schneeball-Schieben',
        'River': 'Fluss',
        'River (clifftop)': 'Fluss (Klippenrand)',
        'River (mouth)': 'Flussmündung',
        'Sea': 'Meer',
        'Sea (rainy days)': 'Meer (Regentage)',
        'Shaking trees': 'Beim Bäumeschütteln',
        'Shaking trees (hardwood or cedar only)': 'Beim Bäumeschütteln (nur Laub-/Nadelbäume)',
        'Underground (dig where noise is loudest)': 'Unterirdisch (grabe wo das Geräusch am lautesten ist)',
        # Time
        'All day': 'Ganztägig',
        'All Day': 'Ganztägig',
        # Weather
        'Any except rain': 'Außer bei Regen',
        'Any weather': 'Jedes Wetter',
        'Rain only': 'Nur bei Regen',
        # Shadow Size
        'Large': 'Groß',
        'Long': 'Lang',
        'Medium': 'Mittel',
        'Small': 'Klein',
        'X-Large': 'Sehr groß',
        'X-Large w/Fin': 'Sehr groß mit Flosse',
        'X-Small': 'Sehr klein',
        'XX-Large': 'Riesig',
        # Catch Difficulty
        'Easy': 'Leicht',
        'Hard': 'Schwer',
        'Very Easy': 'Sehr leicht',
        'Very Hard': 'Sehr schwer',
        # Vision
        'Narrow': 'Eng',
        'Very Narrow': 'Sehr eng',
        'Very Wide': 'Sehr weit',
        'Wide': 'Weit',
        # Movement
        'Fast': 'Schnell',
        'Slow': 'Langsam',
        'Stationary': 'Stationär',
        'Very fast': 'Sehr schnell',
        'Very slow': 'Sehr langsam',
    },
    'es': {
        # Location
        'Disguised on shoreline': 'Camuflado en la orilla',
        'Disguised under trees': 'Camuflado bajo los árboles',
        'Flying': 'Volando',
        'Flying near blue/purple/black flowers': 'Volando cerca de flores azules/moradas/negras',
        'Flying near flowers': 'Volando cerca de flores',
        'Flying near light sources': 'Volando cerca de fuentes de luz',
        'Flying near trash (boots, tires, cans, used fountain fireworks) or rotten turnips': 'Volando cerca de basura (botas, neumáticos, latas, fuegos artificiales usados) o nabos podridos',
        'Flying near water': 'Volando cerca del agua',
        'From hitting rocks': 'Al golpear rocas',
        'On beach rocks': 'En rocas de playa',
        'On flowers': 'En flores',
        'On hardwood/cedar trees': 'En árboles de hoja caduca/cedros',
        'On palm trees': 'En palmeras',
        'On rivers/ponds': 'En ríos/estanques',
        'On rocks/bushes': 'En rocas/arbustos',
        'On rotten turnips or candy': 'En nabos podridos o caramelos',
        'On the ground': 'En el suelo',
        'On tree stumps': 'En tocones de árboles',
        'On trees (any kind)': 'En árboles (cualquier tipo)',
        'On villagers': 'En los vecinos',
        'On white flowers': 'En flores blancas',
        'Pier': 'Muelle',
        'Pond': 'Estanque',
        'Pushing snowballs': 'Empujando bolas de nieve',
        'River': 'Río',
        'River (clifftop)': 'Río (acantilado)',
        'River (mouth)': 'Desembocadura',
        'Sea': 'Mar',
        'Sea (rainy days)': 'Mar (días de lluvia)',
        'Shaking trees': 'Sacudiendo árboles',
        'Shaking trees (hardwood or cedar only)': 'Sacudiendo árboles (solo hoja caduca o cedros)',
        'Underground (dig where noise is loudest)': 'Bajo tierra (cava donde el ruido sea más fuerte)',
        # Time
        'All day': 'Todo el día',
        'All Day': 'Todo el día',
        # Weather
        'Any except rain': 'Cualquiera excepto lluvia',
        'Any weather': 'Cualquier clima',
        'Rain only': 'Solo lluvia',
        # Shadow Size
        'Large': 'Grande',
        'Long': 'Largo',
        'Medium': 'Mediano',
        'Small': 'Pequeño',
        'X-Large': 'Muy grande',
        'X-Large w/Fin': 'Muy grande con aleta',
        'X-Small': 'Muy pequeño',
        'XX-Large': 'Enorme',
        # Catch Difficulty
        'Easy': 'Fácil',
        'Hard': 'Difícil',
        'Very Easy': 'Muy fácil',
        'Very Hard': 'Muy difícil',
        # Vision
        'Narrow': 'Estrecho',
        'Very Narrow': 'Muy estrecho',
        'Very Wide': 'Muy amplio',
        'Wide': 'Amplio',
        # Movement
        'Fast': 'Rápido',
        'Slow': 'Lento',
        'Stationary': 'Estacionario',
        'Very fast': 'Muy rápido',
        'Very slow': 'Muy lento',
    },
    'it': {
        # Location
        'Disguised on shoreline': 'Mimetizzato sulla riva',
        'Disguised under trees': 'Mimetizzato sotto gli alberi',
        'Flying': 'In volo',
        'Flying near blue/purple/black flowers': 'Vola vicino a fiori blu/viola/neri',
        'Flying near flowers': 'Vola vicino ai fiori',
        'Flying near light sources': 'Vola vicino a fonti di luce',
        'Flying near trash (boots, tires, cans, used fountain fireworks) or rotten turnips': 'Vola vicino ai rifiuti (stivali, pneumatici, lattine, fuochi d\'artificio usati) o rape marce',
        'Flying near water': 'Vola vicino all\'acqua',
        'From hitting rocks': 'Colpendo le rocce',
        'On beach rocks': 'Sulle rocce della spiaggia',
        'On flowers': 'Sui fiori',
        'On hardwood/cedar trees': 'Su latifoglie/cedri',
        'On palm trees': 'Sulle palme',
        'On rivers/ponds': 'Su fiumi/stagni',
        'On rocks/bushes': 'Su rocce/cespugli',
        'On rotten turnips or candy': 'Su rape marce o caramelle',
        'On the ground': 'A terra',
        'On tree stumps': 'Sui ceppi',
        'On trees (any kind)': 'Sugli alberi (qualsiasi tipo)',
        'On villagers': 'Sui villici',
        'On white flowers': 'Sui fiori bianchi',
        'Pier': 'Molo',
        'Pond': 'Stagno',
        'Pushing snowballs': 'Spingendo palle di neve',
        'River': 'Fiume',
        'River (clifftop)': 'Fiume (cima della scogliera)',
        'River (mouth)': 'Foce del fiume',
        'Sea': 'Mare',
        'Sea (rainy days)': 'Mare (giorni di pioggia)',
        'Shaking trees': 'Scuotendo gli alberi',
        'Shaking trees (hardwood or cedar only)': 'Scuotendo gli alberi (solo latifoglie o cedri)',
        'Underground (dig where noise is loudest)': 'Sottoterra (scava dove il rumore è più forte)',
        # Time
        'All day': 'Tutto il giorno',
        'All Day': 'Tutto il giorno',
        # Weather
        'Any except rain': 'Qualsiasi tranne pioggia',
        'Any weather': 'Qualsiasi tempo',
        'Rain only': 'Solo pioggia',
        # Shadow Size
        'Large': 'Grande',
        'Long': 'Lungo',
        'Medium': 'Medio',
        'Small': 'Piccolo',
        'X-Large': 'Molto grande',
        'X-Large w/Fin': 'Molto grande con pinna',
        'X-Small': 'Molto piccolo',
        'XX-Large': 'Enorme',
        # Catch Difficulty
        'Easy': 'Facile',
        'Hard': 'Difficile',
        'Very Easy': 'Molto facile',
        'Very Hard': 'Molto difficile',
        # Vision
        'Narrow': 'Stretto',
        'Very Narrow': 'Molto stretto',
        'Very Wide': 'Molto ampio',
        'Wide': 'Ampio',
        # Movement
        'Fast': 'Veloce',
        'Slow': 'Lento',
        'Stationary': 'Fermo',
        'Very fast': 'Molto veloce',
        'Very slow': 'Molto lento',
    },
    'nl': {
        # Location
        'Disguised on shoreline': 'Gecamoufleerd op de kustlijn',
        'Disguised under trees': 'Gecamoufleerd onder bomen',
        'Flying': 'Vliegend',
        'Flying near blue/purple/black flowers': 'Vliegend bij blauwe/paarse/zwarte bloemen',
        'Flying near flowers': 'Vliegend bij bloemen',
        'Flying near light sources': 'Vliegend bij lichtbronnen',
        'Flying near trash (boots, tires, cans, used fountain fireworks) or rotten turnips': 'Vliegend bij afval (laarzen, banden, blikjes, gebruikt vuurwerk) of rotte rapen',
        'Flying near water': 'Vliegend bij water',
        'From hitting rocks': 'Door rotsen te slaan',
        'On beach rocks': 'Op strandrotsen',
        'On flowers': 'Op bloemen',
        'On hardwood/cedar trees': 'Op loofbomen/ceders',
        'On palm trees': 'Op palmbomen',
        'On rivers/ponds': 'Op rivieren/vijvers',
        'On rocks/bushes': 'Op rotsen/struiken',
        'On rotten turnips or candy': 'Op rotte rapen of snoep',
        'On the ground': 'Op de grond',
        'On tree stumps': 'Op boomstronken',
        'On trees (any kind)': 'Op bomen (elk type)',
        'On villagers': 'Op bewoners',
        'On white flowers': 'Op witte bloemen',
        'Pier': 'Pier',
        'Pond': 'Vijver',
        'Pushing snowballs': 'Sneeuwballen duwen',
        'River': 'Rivier',
        'River (clifftop)': 'Rivier (kliftop)',
        'River (mouth)': 'Riviermonding',
        'Sea': 'Zee',
        'Sea (rainy days)': 'Zee (regendagen)',
        'Shaking trees': 'Bomen schudden',
        'Shaking trees (hardwood or cedar only)': 'Bomen schudden (alleen loofbomen of ceders)',
        'Underground (dig where noise is loudest)': 'Ondergronds (graaf waar het geluid het luidst is)',
        # Time
        'All day': 'De hele dag',
        'All Day': 'De hele dag',
        # Weather
        'Any except rain': 'Behalve regen',
        'Any weather': 'Elk weer',
        'Rain only': 'Alleen regen',
        # Shadow Size
        'Large': 'Groot',
        'Long': 'Lang',
        'Medium': 'Gemiddeld',
        'Small': 'Klein',
        'X-Large': 'Extra groot',
        'X-Large w/Fin': 'Extra groot met vin',
        'X-Small': 'Extra klein',
        'XX-Large': 'Enorm',
        # Catch Difficulty
        'Easy': 'Makkelijk',
        'Hard': 'Moeilijk',
        'Very Easy': 'Zeer makkelijk',
        'Very Hard': 'Zeer moeilijk',
        # Vision
        'Narrow': 'Smal',
        'Very Narrow': 'Zeer smal',
        'Very Wide': 'Zeer breed',
        'Wide': 'Breed',
        # Movement
        'Fast': 'Snel',
        'Slow': 'Langzaam',
        'Stationary': 'Stilstaand',
        'Very fast': 'Zeer snel',
        'Very slow': 'Zeer langzaam',
    },
    'ru': {
        # Location
        'Disguised on shoreline': 'Маскируется на берегу',
        'Disguised under trees': 'Маскируется под деревьями',
        'Flying': 'Летает',
        'Flying near blue/purple/black flowers': 'Летает у синих/фиолетовых/чёрных цветов',
        'Flying near flowers': 'Летает у цветов',
        'Flying near light sources': 'Летает у источников света',
        'Flying near trash (boots, tires, cans, used fountain fireworks) or rotten turnips': 'Летает у мусора (ботинки, шины, банки, использованные фейерверки) или гнилой репы',
        'Flying near water': 'Летает у воды',
        'From hitting rocks': 'При ударе по камням',
        'On beach rocks': 'На пляжных камнях',
        'On flowers': 'На цветах',
        'On hardwood/cedar trees': 'На лиственных/кедровых деревьях',
        'On palm trees': 'На пальмах',
        'On rivers/ponds': 'На реках/прудах',
        'On rocks/bushes': 'На камнях/кустах',
        'On rotten turnips or candy': 'На гнилой репе или конфетах',
        'On the ground': 'На земле',
        'On tree stumps': 'На пнях',
        'On trees (any kind)': 'На деревьях (любого типа)',
        'On villagers': 'На жителях',
        'On white flowers': 'На белых цветах',
        'Pier': 'Причал',
        'Pond': 'Пруд',
        'Pushing snowballs': 'Толкая снежки',
        'River': 'Река',
        'River (clifftop)': 'Река (вершина утёса)',
        'River (mouth)': 'Устье реки',
        'Sea': 'Море',
        'Sea (rainy days)': 'Море (дождливые дни)',
        'Shaking trees': 'Трясти деревья',
        'Shaking trees (hardwood or cedar only)': 'Трясти деревья (только лиственные или кедры)',
        'Underground (dig where noise is loudest)': 'Под землёй (копайте где звук громче всего)',
        # Time
        'All day': 'Весь день',
        'All Day': 'Весь день',
        # Weather
        'Any except rain': 'Любая кроме дождя',
        'Any weather': 'Любая погода',
        'Rain only': 'Только дождь',
        # Shadow Size
        'Large': 'Большой',
        'Long': 'Длинный',
        'Medium': 'Средний',
        'Small': 'Маленький',
        'X-Large': 'Очень большой',
        'X-Large w/Fin': 'Очень большой с плавником',
        'X-Small': 'Очень маленький',
        'XX-Large': 'Огромный',
        # Catch Difficulty
        'Easy': 'Легко',
        'Hard': 'Сложно',
        'Very Easy': 'Очень легко',
        'Very Hard': 'Очень сложно',
        # Vision
        'Narrow': 'Узкий',
        'Very Narrow': 'Очень узкий',
        'Very Wide': 'Очень широкий',
        'Wide': 'Широкий',
        # Movement
        'Fast': 'Быстрый',
        'Slow': 'Медленный',
        'Stationary': 'Неподвижный',
        'Very fast': 'Очень быстрый',
        'Very slow': 'Очень медленный',
    },
}


def translate_fossil_detail(value: str, language: str) -> str:
    """Translate a fossil detail value to the user's language.
    
    Used for interaction (Yes/No) and museum room values.
    
    Args:
        value: English value from database
        language: Target language code
    
    Returns:
        Translated value or original if no translation found
    """
    if language == 'en' or not value:
        return value
    
    lang_details = FOSSIL_DETAILS_TRANSLATIONS.get(language, {})
    
    # Try exact match first
    if value in lang_details:
        return lang_details[value]
    
    # Try case-insensitive match
    value_lower = value.lower()
    for eng_val, translated in lang_details.items():
        if eng_val.lower() == value_lower:
            return translated
    
    return value


def translate_villager_detail(value: str, language: str) -> str:
    """Translate a villager detail value to the user's language.
    
    Used for species, personality, hobby, style, and color values.
    
    Args:
        value: English value from database
        language: Target language code
    
    Returns:
        Translated value or original if no translation found
    """
    if language == 'en' or not value:
        return value
    
    lang_details = VILLAGER_DETAILS_TRANSLATIONS.get(language, {})
    
    # Try exact match first
    if value in lang_details:
        return lang_details[value]
    
    # Try case-insensitive match
    value_lower = value.lower()
    for eng_val, translated in lang_details.items():
        if eng_val.lower() == value_lower:
            return translated
    
    return value


def translate_critter_detail(value: str, language: str) -> str:
    """Translate a critter detail value to the user's language.
    
    Used for location, time, weather, shadow size, catch difficulty, vision, and movement.
    
    Args:
        value: English value from database
        language: Target language code
    
    Returns:
        Translated value or original if no translation found
    """
    if language == 'en' or not value:
        return value
    
    lang_details = CRITTER_DETAILS_TRANSLATIONS.get(language, {})
    
    # Try exact match first
    if value in lang_details:
        return lang_details[value]
    
    # Try case-insensitive match
    value_lower = value.lower()
    for eng_val, translated in lang_details.items():
        if eng_val.lower() == value_lower:
            return translated
    
    return value


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
        
        # Fossil labels
        'fossil_group': 'Fossil Group',
        'museum_info': 'Museum Info',
        'museum': 'Museum',
        'interaction': 'Interaction',
        'points': 'points',
        'museum_fossil': 'Museum Fossil',
        'size': 'Size',
        
        # Recipe labels
        'diy_recipe': 'DIY Recipe',
        'food_recipe': 'Food Recipe',
        'ingredients': 'Ingredients',
        'unknown_category': 'Unknown Category',
        
        # Critter labels
        'location': 'Location',
        'shadow_size': 'Shadow Size',
        'time_label': 'Time',
        'catch_info': 'Catch Info',
        'difficulty': 'Difficulty',
        'vision': 'Vision',
        'movement': 'Movement',
        'type_fish': 'Fish',
        'type_bug': 'Bug',
        'type_sea_creature': 'Sea Creature',
        
        # Villager labels
        'species': 'Species',
        'personality': 'Personality',
        'hobby': 'Hobby',
        'birthday': 'Birthday',
        'catchphrase': 'Catchphrase',
        'preferences': 'Preferences',
        'style': 'Style',
        'colors': 'Colors',
        'favorites': 'Favorites',
        'song': 'Song',
        'saying': 'Saying',
        
        # Availability view
        'availability': 'Availability',
        'hemisphere': 'Hemisphere',
        'month': 'Month',
        'northern_hemisphere': 'Northern Hemisphere',
        'southern_hemisphere': 'Southern Hemisphere',
        'available': 'Available',
        'not_available_in': 'Not Available in {month}',
        'full_year_overview': 'Full Year Overview',
        'additional_info': 'Additional Info',
        'weather': 'Weather',
        'view_availability': 'View Availability',
        'back_to_details': 'Back to Details',
        'choose_hemisphere': 'Choose hemisphere...',
        'choose_month': 'Choose month...',
        # Month names
        'january': 'January',
        'february': 'February',
        'march': 'March',
        'april': 'April',
        'may': 'May',
        'june': 'June',
        'july': 'July',
        'august': 'August',
        'september': 'September',
        'october': 'October',
        'november': 'November',
        'december': 'December',
        
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
        
        # Fossil labels
        'fossil_group': '化石グループ',
        'museum_info': '博物館情報',
        'museum': '博物館',
        'interaction': 'インタラクション',
        'points': 'ポイント',
        'museum_fossil': '博物館の化石',
        'size': 'サイズ',
        
        # Recipe labels
        'diy_recipe': 'DIYレシピ',
        'food_recipe': '料理レシピ',
        'ingredients': '材料',
        'unknown_category': '不明なカテゴリー',
        
        # Critter labels
        'location': '生息地',
        'shadow_size': '魚影',
        'time_label': '時間',
        'catch_info': '捕獲情報',
        'difficulty': '難易度',
        'vision': '視野',
        'movement': '動き',
        'type_fish': 'さかな',
        'type_bug': 'ムシ',
        'type_sea_creature': 'うみのさち',
        
        # Villager labels
        'species': '種族',
        'personality': '性格',
        'hobby': '趣味',
        'birthday': '誕生日',
        'catchphrase': '口ぐせ',
        'preferences': '好み',
        'style': 'スタイル',
        'colors': '色',
        'favorites': 'お気に入り',
        'song': '曲',
        'saying': '座右の銘',
        
        # Availability view
        'availability': '出現時期',
        'hemisphere': '半球',
        'month': '月',
        'northern_hemisphere': '北半球',
        'southern_hemisphere': '南半球',
        'available': '出現',
        'not_available_in': '{month}には出現しません',
        'full_year_overview': '年間カレンダー',
        'additional_info': '追加情報',
        'weather': '天気',
        'view_availability': '出現時期を見る',
        'back_to_details': '詳細に戻る',
        'choose_hemisphere': '半球を選択...',
        'choose_month': '月を選択...',
        # Month names
        'january': '1月',
        'february': '2月',
        'march': '3月',
        'april': '4月',
        'may': '5月',
        'june': '6月',
        'july': '7月',
        'august': '8月',
        'september': '9月',
        'october': '10月',
        'november': '11月',
        'december': '12月',
        
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
        
        # Fossil labels
        'fossil_group': '化石组',
        'museum_info': '博物馆信息',
        'museum': '博物馆',
        'interaction': '互动',
        'points': '点',
        'museum_fossil': '博物馆化石',
        'size': '尺寸',
        
        # Recipe labels
        'diy_recipe': 'DIY配方',
        'food_recipe': '料理配方',
        'ingredients': '材料',
        'unknown_category': '未知分类',
        
        # Critter labels
        'location': '位置',
        'shadow_size': '阴影大小',
        'time_label': '时间',
        'catch_info': '捕捉信息',
        'difficulty': '难度',
        'vision': '视野',
        'movement': '移动',
        'type_fish': '鱼类',
        'type_bug': '虫类',
        'type_sea_creature': '海洋生物',
        
        # Villager labels
        'species': '种族',
        'personality': '性格',
        'hobby': '爱好',
        'birthday': '生日',
        'catchphrase': '口头禅',
        'preferences': '偏好',
        'style': '风格',
        'colors': '颜色',
        'favorites': '最爱',
        'song': '歌曲',
        'saying': '座右铭',
        
        # Availability view
        'availability': '出现时间',
        'hemisphere': '半球',
        'month': '月份',
        'northern_hemisphere': '北半球',
        'southern_hemisphere': '南半球',
        'available': '可捕捉',
        'not_available_in': '{month}不出现',
        'full_year_overview': '全年概览',
        'additional_info': '额外信息',
        'weather': '天气',
        'view_availability': '查看出现时间',
        'back_to_details': '返回详情',
        'choose_hemisphere': '选择半球...',
        'choose_month': '选择月份...',
        # Month names
        'january': '1月',
        'february': '2月',
        'march': '3月',
        'april': '4月',
        'may': '5月',
        'june': '6月',
        'july': '7月',
        'august': '8月',
        'september': '9月',
        'october': '10月',
        'november': '11月',
        'december': '12月',
        
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
        
        # Fossil labels
        'fossil_group': '화석 그룹',
        'museum_info': '박물관 정보',
        'museum': '박물관',
        'interaction': '인터랙션',
        'points': '포인트',
        'museum_fossil': '박물관 화석',
        'size': '크기',
        
        # Recipe labels
        'diy_recipe': 'DIY 레시피',
        'food_recipe': '요리 레시피',
        'ingredients': '재료',
        'unknown_category': '알 수 없는 카테고리',
        
        # Critter labels
        'location': '위치',
        'shadow_size': '그림자 크기',
        'time_label': '시간',
        'catch_info': '포획 정보',
        'difficulty': '난이도',
        'vision': '시야',
        'movement': '이동',
        'type_fish': '물고기',
        'type_bug': '곤충',
        'type_sea_creature': '해산물',
        
        # Villager labels
        'species': '종족',
        'personality': '성격',
        'hobby': '취미',
        'birthday': '생일',
        'catchphrase': '말버릇',
        'preferences': '취향',
        'style': '스타일',
        'colors': '색상',
        'favorites': '좋아하는 것',
        'song': '노래',
        'saying': '좌우명',
        
        # Availability view
        'availability': '출현 시기',
        'hemisphere': '반구',
        'month': '월',
        'northern_hemisphere': '북반구',
        'southern_hemisphere': '남반구',
        'available': '출현',
        'not_available_in': '{month}에는 출현하지 않습니다',
        'full_year_overview': '연간 개요',
        'additional_info': '추가 정보',
        'weather': '날씨',
        'view_availability': '출현 시기 보기',
        'back_to_details': '상세 정보로',
        'choose_hemisphere': '반구 선택...',
        'choose_month': '월 선택...',
        # Month names
        'january': '1월',
        'february': '2월',
        'march': '3월',
        'april': '4월',
        'may': '5월',
        'june': '6월',
        'july': '7월',
        'august': '8월',
        'september': '9월',
        'october': '10월',
        'november': '11월',
        'december': '12월',
        
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
        
        # Fossil labels
        'fossil_group': 'Groupe de fossiles',
        'museum_info': 'Infos musée',
        'museum': 'Musée',
        'interaction': 'Interaction',
        'points': 'points',
        'museum_fossil': 'Fossile du musée',
        'size': 'Taille',
        
        # Recipe labels
        'diy_recipe': 'Recette de bricolage',
        'food_recipe': 'Recette de cuisine',
        'ingredients': 'Ingrédients',
        'unknown_category': 'Catégorie inconnue',
        
        # Critter labels
        'location': 'Emplacement',
        'shadow_size': 'Taille de l\'ombre',
        'time_label': 'Horaire',
        'catch_info': 'Infos de capture',
        'difficulty': 'Difficulté',
        'vision': 'Vision',
        'movement': 'Mouvement',
        'type_fish': 'Poisson',
        'type_bug': 'Insecte',
        'type_sea_creature': 'Créature marine',
        
        # Villager labels
        'species': 'Espèce',
        'personality': 'Personnalité',
        'hobby': 'Loisir',
        'birthday': 'Anniversaire',
        'catchphrase': 'Phrase fétiche',
        'preferences': 'Préférences',
        'style': 'Style',
        'colors': 'Couleurs',
        'favorites': 'Favoris',
        'song': 'Chanson',
        'saying': 'Citation',
        
        # Availability view
        'availability': 'Disponibilité',
        'hemisphere': 'Hémisphère',
        'month': 'Mois',
        'northern_hemisphere': 'Hémisphère Nord',
        'southern_hemisphere': 'Hémisphère Sud',
        'available': 'Disponible',
        'not_available_in': 'Pas disponible en {month}',
        'full_year_overview': "Aperçu de l'année",
        'additional_info': 'Infos supplémentaires',
        'weather': 'Météo',
        'view_availability': 'Voir la disponibilité',
        'back_to_details': 'Retour aux détails',
        'choose_hemisphere': "Choisir l'hémisphère...",
        'choose_month': 'Choisir le mois...',
        # Month names
        'january': 'Janvier',
        'february': 'Février',
        'march': 'Mars',
        'april': 'Avril',
        'may': 'Mai',
        'june': 'Juin',
        'july': 'Juillet',
        'august': 'Août',
        'september': 'Septembre',
        'october': 'Octobre',
        'november': 'Novembre',
        'december': 'Décembre',
        
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
        
        # Fossil labels
        'fossil_group': 'Fossilgruppe',
        'museum_info': 'Museumsinfo',
        'museum': 'Museum',
        'interaction': 'Interaktion',
        'points': 'Punkte',
        'museum_fossil': 'Museumsfossil',
        'size': 'Größe',
        
        # Recipe labels
        'diy_recipe': 'Heimwerker-Rezept',
        'food_recipe': 'Kochrezept',
        'ingredients': 'Zutaten',
        'unknown_category': 'Unbekannte Kategorie',
        
        # Critter labels
        'location': 'Fundort',
        'shadow_size': 'Schattengröße',
        'time_label': 'Zeit',
        'catch_info': 'Fang-Info',
        'difficulty': 'Schwierigkeit',
        'vision': 'Sicht',
        'movement': 'Bewegung',
        'type_fish': 'Fisch',
        'type_bug': 'Insekt',
        'type_sea_creature': 'Meerestier',
        
        # Villager labels
        'species': 'Spezies',
        'personality': 'Persönlichkeit',
        'hobby': 'Hobby',
        'birthday': 'Geburtstag',
        'catchphrase': 'Spruch',
        'preferences': 'Vorlieben',
        'style': 'Stil',
        'colors': 'Farben',
        'favorites': 'Favoriten',
        'song': 'Lied',
        'saying': 'Motto',
        
        # Availability view
        'availability': 'Verfügbarkeit',
        'hemisphere': 'Hemisphäre',
        'month': 'Monat',
        'northern_hemisphere': 'Nordhalbkugel',
        'southern_hemisphere': 'Südhalbkugel',
        'available': 'Verfügbar',
        'not_available_in': 'Nicht verfügbar im {month}',
        'full_year_overview': 'Jahresübersicht',
        'additional_info': 'Weitere Infos',
        'weather': 'Wetter',
        'view_availability': 'Verfügbarkeit anzeigen',
        'back_to_details': 'Zurück zu Details',
        'choose_hemisphere': 'Hemisphäre wählen...',
        'choose_month': 'Monat wählen...',
        # Month names
        'january': 'Januar',
        'february': 'Februar',
        'march': 'März',
        'april': 'April',
        'may': 'Mai',
        'june': 'Juni',
        'july': 'Juli',
        'august': 'August',
        'september': 'September',
        'october': 'Oktober',
        'november': 'November',
        'december': 'Dezember',
        
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
        
        # Fossil labels
        'fossil_group': 'Grupo de fósiles',
        'museum_info': 'Info del museo',
        'museum': 'Museo',
        'interaction': 'Interacción',
        'points': 'puntos',
        'museum_fossil': 'Fósil de museo',
        'size': 'Tamaño',
        
        # Recipe labels
        'diy_recipe': 'Receta de bricolaje',
        'food_recipe': 'Receta de cocina',
        'ingredients': 'Ingredientes',
        'unknown_category': 'Categoría desconocida',
        
        # Critter labels
        'location': 'Ubicación',
        'shadow_size': 'Tamaño de sombra',
        'time_label': 'Horario',
        'catch_info': 'Info de captura',
        'difficulty': 'Dificultad',
        'vision': 'Visión',
        'movement': 'Movimiento',
        'type_fish': 'Pez',
        'type_bug': 'Insecto',
        'type_sea_creature': 'Criatura marina',
        
        # Villager labels
        'species': 'Especie',
        'personality': 'Personalidad',
        'hobby': 'Afición',
        'birthday': 'Cumpleaños',
        'catchphrase': 'Frase',
        'preferences': 'Preferencias',
        'style': 'Estilo',
        'colors': 'Colores',
        'favorites': 'Favoritos',
        'song': 'Canción',
        'saying': 'Lema',
        
        # Availability view
        'availability': 'Disponibilidad',
        'hemisphere': 'Hemisferio',
        'month': 'Mes',
        'northern_hemisphere': 'Hemisferio Norte',
        'southern_hemisphere': 'Hemisferio Sur',
        'available': 'Disponible',
        'not_available_in': 'No disponible en {month}',
        'full_year_overview': 'Resumen anual',
        'additional_info': 'Info adicional',
        'weather': 'Clima',
        'view_availability': 'Ver disponibilidad',
        'back_to_details': 'Volver a detalles',
        'choose_hemisphere': 'Elegir hemisferio...',
        'choose_month': 'Elegir mes...',
        # Month names
        'january': 'Enero',
        'february': 'Febrero',
        'march': 'Marzo',
        'april': 'Abril',
        'may': 'Mayo',
        'june': 'Junio',
        'july': 'Julio',
        'august': 'Agosto',
        'september': 'Septiembre',
        'october': 'Octubre',
        'november': 'Noviembre',
        'december': 'Diciembre',
        
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
        
        # Fossil labels
        'fossil_group': 'Gruppo di fossili',
        'museum_info': 'Info museo',
        'museum': 'Museo',
        'interaction': 'Interazione',
        'points': 'punti',
        'museum_fossil': 'Fossile del museo',
        'size': 'Dimensione',
        
        # Recipe labels
        'diy_recipe': 'Ricetta fai da te',
        'food_recipe': 'Ricetta di cucina',
        'ingredients': 'Ingredienti',
        'unknown_category': 'Categoria sconosciuta',
        
        # Critter labels
        'location': 'Posizione',
        'shadow_size': 'Dimensione ombra',
        'time_label': 'Orario',
        'catch_info': 'Info cattura',
        'difficulty': 'Difficoltà',
        'vision': 'Visione',
        'movement': 'Movimento',
        'type_fish': 'Pesce',
        'type_bug': 'Insetto',
        'type_sea_creature': 'Creatura marina',
        
        # Villager labels
        'species': 'Specie',
        'personality': 'Personalità',
        'hobby': 'Hobby',
        'birthday': 'Compleanno',
        'catchphrase': 'Tormentone',
        'preferences': 'Preferenze',
        'style': 'Stile',
        'colors': 'Colori',
        'favorites': 'Preferiti',
        'song': 'Canzone',
        'saying': 'Motto',
        
        # Availability view
        'availability': 'Disponibilità',
        'hemisphere': 'Emisfero',
        'month': 'Mese',
        'northern_hemisphere': 'Emisfero Nord',
        'southern_hemisphere': 'Emisfero Sud',
        'available': 'Disponibile',
        'not_available_in': 'Non disponibile a {month}',
        'full_year_overview': "Panoramica dell'anno",
        'additional_info': 'Info aggiuntive',
        'weather': 'Meteo',
        'view_availability': 'Vedi disponibilità',
        'back_to_details': 'Torna ai dettagli',
        'choose_hemisphere': "Scegli l'emisfero...",
        'choose_month': 'Scegli il mese...',
        # Month names
        'january': 'Gennaio',
        'february': 'Febbraio',
        'march': 'Marzo',
        'april': 'Aprile',
        'may': 'Maggio',
        'june': 'Giugno',
        'july': 'Luglio',
        'august': 'Agosto',
        'september': 'Settembre',
        'october': 'Ottobre',
        'november': 'Novembre',
        'december': 'Dicembre',
        
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
        
        # Fossil labels
        'fossil_group': 'Fossielgroep',
        'museum_info': 'Museum info',
        'museum': 'Museum',
        'interaction': 'Interactie',
        'points': 'punten',
        'museum_fossil': 'Museumfossiel',
        'size': 'Grootte',
        
        # Recipe labels
        'diy_recipe': 'Doe-het-zelf recept',
        'food_recipe': 'Kookrecept',
        'ingredients': 'Ingrediënten',
        'unknown_category': 'Onbekende categorie',
        
        # Critter labels
        'location': 'Locatie',
        'shadow_size': 'Schaduwgrootte',
        'time_label': 'Tijd',
        'catch_info': 'Vangst info',
        'difficulty': 'Moeilijkheid',
        'vision': 'Zicht',
        'movement': 'Beweging',
        'type_fish': 'Vis',
        'type_bug': 'Insect',
        'type_sea_creature': 'Zeedier',
        
        # Villager labels
        'species': 'Soort',
        'personality': 'Persoonlijkheid',
        'hobby': 'Hobby',
        'birthday': 'Verjaardag',
        'catchphrase': 'Stopwoordje',
        'preferences': 'Voorkeuren',
        'style': 'Stijl',
        'colors': 'Kleuren',
        'favorites': 'Favorieten',
        'song': 'Liedje',
        'saying': 'Motto',
        
        # Availability view
        'availability': 'Beschikbaarheid',
        'hemisphere': 'Halfrond',
        'month': 'Maand',
        'northern_hemisphere': 'Noordelijk halfrond',
        'southern_hemisphere': 'Zuidelijk halfrond',
        'available': 'Beschikbaar',
        'not_available_in': 'Niet beschikbaar in {month}',
        'full_year_overview': 'Jaaroverzicht',
        'additional_info': 'Extra info',
        'weather': 'Weer',
        'view_availability': 'Bekijk beschikbaarheid',
        'back_to_details': 'Terug naar details',
        'choose_hemisphere': 'Kies halfrond...',
        'choose_month': 'Kies maand...',
        # Month names
        'january': 'Januari',
        'february': 'Februari',
        'march': 'Maart',
        'april': 'April',
        'may': 'Mei',
        'june': 'Juni',
        'july': 'Juli',
        'august': 'Augustus',
        'september': 'September',
        'october': 'Oktober',
        'november': 'November',
        'december': 'December',
        
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
        
        # Fossil labels
        'fossil_group': 'Группа окаменелостей',
        'museum_info': 'Инфо о музее',
        'museum': 'Музей',
        'interaction': 'Взаимодействие',
        'points': 'очков',
        'museum_fossil': 'Музейная окаменелость',
        'size': 'Размер',
        
        # Recipe labels
        'diy_recipe': 'Рецепт DIY',
        'food_recipe': 'Рецепт еды',
        'ingredients': 'Ингредиенты',
        'unknown_category': 'Неизвестная категория',
        
        # Critter labels
        'location': 'Место',
        'shadow_size': 'Размер тени',
        'time_label': 'Время',
        'catch_info': 'Инфо о ловле',
        'difficulty': 'Сложность',
        'vision': 'Зрение',
        'movement': 'Движение',
        'type_fish': 'Рыба',
        'type_bug': 'Насекомое',
        'type_sea_creature': 'Морское существо',
        
        # Villager labels
        'species': 'Вид',
        'personality': 'Характер',
        'hobby': 'Хобби',
        'birthday': 'День рождения',
        'catchphrase': 'Коронная фраза',
        'preferences': 'Предпочтения',
        'style': 'Стиль',
        'colors': 'Цвета',
        'favorites': 'Избранное',
        'song': 'Песня',
        'saying': 'Девиз',
        
        # Availability view
        'availability': 'Доступность',
        'hemisphere': 'Полушарие',
        'month': 'Месяц',
        'northern_hemisphere': 'Северное полушарие',
        'southern_hemisphere': 'Южное полушарие',
        'available': 'Доступно',
        'not_available_in': 'Недоступно в {month}',
        'full_year_overview': 'Годовой обзор',
        'additional_info': 'Доп. информация',
        'weather': 'Погода',
        'view_availability': 'Посмотреть доступность',
        'back_to_details': 'Назад к деталям',
        'choose_hemisphere': 'Выберите полушарие...',
        'choose_month': 'Выберите месяц...',
        # Month names
        'january': 'Январь',
        'february': 'Февраль',
        'march': 'Март',
        'april': 'Апрель',
        'may': 'Май',
        'june': 'Июнь',
        'july': 'Июль',
        'august': 'Август',
        'september': 'Сентябрь',
        'october': 'Октябрь',
        'november': 'Ноябрь',
        'december': 'Декабрь',
        
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
    
    # Fossil labels
    @property
    def fossil_group(self) -> str:
        return self._get('fossil_group')
    
    @property
    def museum_info(self) -> str:
        return self._get('museum_info')
    
    @property
    def museum(self) -> str:
        return self._get('museum')
    
    @property
    def interaction(self) -> str:
        return self._get('interaction')
    
    @property
    def points(self) -> str:
        return self._get('points')
    
    @property
    def museum_fossil(self) -> str:
        return self._get('museum_fossil')
    
    @property
    def size(self) -> str:
        return self._get('size')
    
    # Recipe labels
    @property
    def diy_recipe(self) -> str:
        return self._get('diy_recipe')
    
    @property
    def food_recipe(self) -> str:
        return self._get('food_recipe')
    
    @property
    def ingredients(self) -> str:
        return self._get('ingredients')
    
    @property
    def unknown_category(self) -> str:
        return self._get('unknown_category')
    
    # Villager labels
    @property
    def species(self) -> str:
        return self._get('species')
    
    @property
    def personality(self) -> str:
        return self._get('personality')
    
    @property
    def hobby(self) -> str:
        return self._get('hobby')
    
    @property
    def birthday(self) -> str:
        return self._get('birthday')
    
    @property
    def catchphrase(self) -> str:
        return self._get('catchphrase')
    
    @property
    def preferences(self) -> str:
        return self._get('preferences')
    
    @property
    def style(self) -> str:
        return self._get('style')
    
    @property
    def colors(self) -> str:
        return self._get('colors')
    
    @property
    def favorites(self) -> str:
        return self._get('favorites')
    
    @property
    def song(self) -> str:
        return self._get('song')
    
    @property
    def saying(self) -> str:
        return self._get('saying')
    
    # Critter labels
    @property
    def location(self) -> str:
        return self._get('location')
    
    @property
    def shadow_size(self) -> str:
        return self._get('shadow_size')
    
    @property
    def time_label(self) -> str:
        return self._get('time_label')
    
    @property
    def catch_info(self) -> str:
        return self._get('catch_info')
    
    @property
    def difficulty(self) -> str:
        return self._get('difficulty')
    
    @property
    def vision(self) -> str:
        return self._get('vision')
    
    @property
    def movement(self) -> str:
        return self._get('movement')
    
    @property
    def type_fish(self) -> str:
        return self._get('type_fish')
    
    @property
    def type_bug(self) -> str:
        return self._get('type_bug')
    
    @property
    def type_sea_creature(self) -> str:
        return self._get('type_sea_creature')
    
    # Availability view
    @property
    def availability(self) -> str:
        return self._get('availability')
    
    @property
    def hemisphere(self) -> str:
        return self._get('hemisphere')
    
    @property
    def month_label(self) -> str:
        return self._get('month')
    
    @property
    def northern_hemisphere(self) -> str:
        return self._get('northern_hemisphere')
    
    @property
    def southern_hemisphere(self) -> str:
        return self._get('southern_hemisphere')
    
    @property
    def available(self) -> str:
        return self._get('available')
    
    def not_available_in(self, month: str) -> str:
        """Get 'Not Available in {month}' with the month name substituted"""
        return self._get('not_available_in').format(month=month)
    
    @property
    def full_year_overview(self) -> str:
        return self._get('full_year_overview')
    
    @property
    def additional_info(self) -> str:
        return self._get('additional_info')
    
    @property
    def weather(self) -> str:
        return self._get('weather')
    
    @property
    def view_availability(self) -> str:
        return self._get('view_availability')
    
    @property
    def back_to_details(self) -> str:
        return self._get('back_to_details')
    
    @property
    def choose_hemisphere(self) -> str:
        return self._get('choose_hemisphere')
    
    @property
    def choose_month(self) -> str:
        return self._get('choose_month')
    
    def get_month_name(self, month_key: str) -> str:
        """Get localized month name from month key (jan, feb, etc.)"""
        month_map = {
            'jan': 'january', 'feb': 'february', 'mar': 'march', 'apr': 'april',
            'may': 'may', 'jun': 'june', 'jul': 'july', 'aug': 'august',
            'sep': 'september', 'oct': 'october', 'nov': 'november', 'dec': 'december'
        }
        return self._get(month_map.get(month_key, month_key))
    
    def get_month_short(self, month_key: str) -> str:
        """Get abbreviated month name (first 3 chars of localized name)"""
        return self.get_month_name(month_key)[:3]
    
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
