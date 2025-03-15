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
