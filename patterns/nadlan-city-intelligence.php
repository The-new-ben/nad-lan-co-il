<?php
/**
 * Title: מודיעין ערים
 * Slug: nadlan-revenue/city-intelligence
 * Categories: nadlan-row
 * Description: שתי עמודות — מקום למפה/גרף ורשימת ערים מובילות.
 */
?>
<!-- wp:group {"tagName":"section","className":"nadlan-city-intel","layout":{"type":"constrained"}} -->
<section class="wp-block-group nadlan-city-intel">
  <!-- wp:heading {"level":2} --><h2>מה קורה בכל עיר.</h2><!-- /wp:heading -->
  <!-- wp:separator {"className":"gold-rule gold-rule--sm"} --><hr class="wp-block-separator gold-rule gold-rule--sm"/><!-- /wp:separator -->

  <!-- wp:columns -->
  <div class="wp-block-columns">

    <!-- wp:column {"width":"60%"} -->
    <div class="wp-block-column" style="flex-basis:60%">
      <div class="map-widget" style="min-block-size:420px">
        <div class="map-canvas" aria-label="מפת ישראל מונוכרומטית"></div>
        <div class="map-zoom"><button aria-label="הגדלה">+</button><button aria-label="הקטנה">−</button></div>
      </div>
    </div>
    <!-- /wp:column -->

    <!-- wp:column {"width":"40%"} -->
    <div class="wp-block-column" style="flex-basis:40%">
      <table class="table-hairline">
        <thead><tr><th>עיר</th><th class="tabular">חציון ₪/מ״ר</th><th class="tabular">Δ שנתי</th></tr></thead>
        <tbody>
          <tr><td><a class="link-luxury" href="/cities/tel-aviv/">תל אביב–יפו</a></td><td class="tabular">52,800</td><td class="tabular">−2.4%</td></tr>
          <tr><td><a class="link-luxury" href="/cities/jerusalem/">ירושלים</a></td><td class="tabular">32,100</td><td class="tabular">+0.6%</td></tr>
          <tr><td><a class="link-luxury" href="/cities/haifa/">חיפה</a></td><td class="tabular">18,900</td><td class="tabular">−1.1%</td></tr>
          <tr><td><a class="link-luxury" href="/cities/ramat-gan/">רמת גן</a></td><td class="tabular">38,400</td><td class="tabular">−1.9%</td></tr>
          <tr><td><a class="link-luxury" href="/cities/herzliya/">הרצליה</a></td><td class="tabular">44,200</td><td class="tabular">−0.8%</td></tr>
        </tbody>
      </table>
      <p><a class="link-luxury" href="/cities/">כל הערים ←</a></p>
    </div>
    <!-- /wp:column -->

  </div>
  <!-- /wp:columns -->
</section>
<!-- /wp:group -->