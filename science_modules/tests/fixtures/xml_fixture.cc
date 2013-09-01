#include "xml_fixture.hh"

const char* xml_fixture::lc_tmpl = R"(
<tao>
  <workflow>
    <light-cone id="light-cone">
      <geometry>light-cone</geometry>
      <box-repetition>%1%</box-repetition>
      <rng-seed>%2%</rng-seed>
      <redshift-min>%3%</redshift-min>
      <redshift-max>%4%</redshift-max>
      <ra-min>%5%</ra-min>
      <ra-max>%6%</ra-max>
      <dec-min>%7%</dec-min>
      <dec-max>%8%</dec-max>
      <output-fields>
        <item>pos_x</item>
        <item>pos_y</item>
        <item>pos_z</item>
      </output-fields>
    </light-cone>
    <record-filter>
      <filter>
        <filter-attribute>%9%</filter-attribute>
        <filter-min>%10%</filter-min>
        <filter-max>%11%</filter-max>
      </filter>
    </record-filter>
  </workflow>
</tao>
)";

const char* xml_fixture::box_tmpl = R"(
<tao>
  <workflow>
    <light-cone id="light-cone">
      <geometry>box</geometry>
      <rng-seed>%1%</rng-seed>
      <query-box-size>%2%</query-box-size>
      <redshift>%3%</redshift>
      <output-fields>
        <item>pos_x</item>
        <item>pos_y</item>
        <item>pos_z</item>
      </output-fields>
    </light-cone>
    <record-filter>
      <filter>
        <filter-attribute>%4%</filter-attribute>
        <filter-min>%5%</filter-min>
        <filter-max>%6%</filter-max>
      </filter>
    </record-filter>
  </workflow>
</tao>
)";
