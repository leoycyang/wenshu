CREATE TABLE wenshu(
    -- implicit to sqlite3: rowid INTEGER PRIMARY KEY
    source_url TEXT, -- 原始链接
    case_id TEXT, -- 案号
    case_title TEXT, -- 案件名称
    court TEXT, -- 法院
    location TEXT, -- 所属地区
    case_type TEXT, -- 案件类型
    case_type_code TEXT, -- 案件类型编码
    source TEXT, -- 来源
    procedure TEXT, -- 审理程序
    ruling_date DATE, -- 裁判日期
    publication_date DATE, -- 公开日期
    parties TEXT, -- 当事人
    cause_of_action TEXT, -- 案由
    legal_basis TEXT, -- 法律依据
    full_text TEXT -- 全文
);

CREATE TABLE guiding_cases (
    id INTEGER NOT NULL PRIMARY KEY, -- 序号
    case_title TEXT NOT NULL, -- 案件名称
    series INTEGER NOT NULL, -- 批次 *** CONVERT!
    guiding_case_number INTEGER NOT NULL UNIQUE, -- 指导案例件编号 *** CONVERT!
    publication_date DATE NOT NULL, -- 发布时间 **** CONVERT
    keywords TEXT, -- 关键词 *** MIULTIPLE
    related_codes TEXT -- 相关法条 **** MULTIPLE & CLEAN
    -- first_trial_court TEXT, -- 一审法院
    -- first_trial_case_id TEXT, -- 一审案号
    -- first_trial_ruling_date DATE, -- 二审裁判日期
    -- second_trial_court TEXT, -- 二审法院
    -- second_trial_case_id TEXT, -- 二审案号
    -- second_trial_ruling_date DATE, -- 二审裁判日期
    -- death_penalty_review_case_id TEXT, -- 死刑复核_案号
    -- death_penalty_review_ruling_date DATE, -- 死刑复核_裁判日期
    -- retrial_court TEXT, -- 重审_法院
    -- retrial_case_id TEXT, -- 重审_案号
    -- retrial_ruling_date DATE, -- 重审_裁判日期
    -- review_trial_court TEXT, -- 再审_法院 **** MULTIPLE
    -- review_trial_case_id TEXT, -- 再审_案号 **** MULTIPLE
    -- review_trial_ruling_date TEXT, -- 再审_裁判日期 **** MULTIPLE
    -- "国家赔偿（先行处理程序）_机关" TEXT,
    -- "国家赔偿（先行处理程序）_案号" TEXT,
    -- "国家赔偿（先行处理程序）_决定日期" TEXT,
    -- "国家赔偿（司法赔偿复议程序）_机关" TEXT,
    -- "国家赔偿（司法赔偿复议程序）_案号" TEXT,
    -- "国家赔偿（司法赔偿复议程序）_决定日期" TEXT,
    -- "国家赔偿（法院赔偿委员会处理程序）_法院" TEXT,
    -- "国家赔偿（法院赔偿委员会处理程序）_案号" TEXT,
    -- "国家赔偿（法院赔偿委员会处理程序）_决定日期" TEXT,
    -- "申请执行_法院" TEXT,
    -- "申请执行_案号" TEXT,
    -- "申请执行_裁定日期" TEXT,
    -- "执行复议_法院" TEXT,
    -- "执行复议_案号" TEXT,
    -- "执行复议_裁定日期" TEXT,
    -- "执行申诉_法院" TEXT,
    -- "执行申诉_案号" TEXT,
    -- "执行申诉_裁定日期" TEXT,
    -- "生效裁判审判人员_Unnamed: 39_level_1" TEXT,
    -- "生效裁判审判人员_Unnamed: 40_level_1" TEXT,
    -- "生效裁判审判人员_Unnamed: 41_level_1" TEXT,
    -- "生效裁判审判人员_Unnamed: 42_level_1" TEXT,
    -- "生效裁判审判人员_Unnamed: 43_level_1" TEXT,
    -- "生效裁判审判人员_Unnamed: 44_level_1" TEXT,
    -- "生效裁判审判人员_Unnamed: 45_level_1" TEXT,
    -- "发布原因_Unnamed: 46_level_1" TEXT,
    -- "是否创制新的规则_Unnamed: 47_level_1" TEXT,
    -- "是否创制新的规则_Unnamed: 48_level_1" TEXT,
    -- "被引用次数_Unnamed: 49_level_1" TEXT,
    -- "被引用次数_Unnamed: 50_level_1" TEXT,
    -- "应当被参照次数_法条+关键词检索" TEXT,
    -- "应当被参照次数_仅法条检索" TEXT,
    -- "引用指导案例的文书占总的应当引用文书总数的百分比_法条+关键词检索" TEXT,
    -- "引用指导案例的文书占总的应当引用文书总数的百分比_仅法条检索" TEXT,
    -- "应当被参照次数_全文法条检索" TEXT,
    -- "引用指导案例的文书占总的应当引用文书总数的百分比_全文法条检索" TEXT,
    -- "原始判决法院层级_Unnamed: 57_level_1" TEXT,
    -- "原始判决省份_Unnamed: 58_level_1" TEXT
);
