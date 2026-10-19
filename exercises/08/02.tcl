set first [dict create id A]
 set second [dict create id B owner ""]
 set third [dict create id C owner "周 月"]
 set notices {}
 # 遍历三条记录，区分字段不存在和字段值为空
 puts [join $notices "\n"]
