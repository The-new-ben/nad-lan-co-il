<?php
/**
 * Fallback template.
 */
get_header();
?>
<main class="section">
    <div class="container">
        <?php if (have_posts()) : ?>
            <?php while (have_posts()) : the_post(); ?>
                <article <?php post_class('card'); ?>>
                    <h1><?php the_title(); ?></h1>
                    <?php the_content(); ?>
                </article>
            <?php endwhile; ?>
        <?php else : ?>
            <h1>לא נמצא תוכן</h1>
            <p>נוסיף כאן עמודי נדל״ן מסחריים, מחשבונים ומדריכים.</p>
        <?php endif; ?>
    </div>
</main>
<?php
get_footer();
