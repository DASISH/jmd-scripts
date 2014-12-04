create INDEX idx_pr_package_id ON package_role ( package_id );
create INDEX idx_mr_table_id ON member_revision ( table_id );
create INDEX idx_mr_continuity_id ON member_revision ( continuity_id );
create INDEX idx_mr_revision_id ON member_revision ( revision_id );
--create INDEX idx_per_continuity_id ON package_extra_revision ( continuity_id );
create INDEX idx_per_revision_id ON package_extra_revision ( revision_id );
create INDEX idx_pe_package_id ON package_extra ( package_id );

