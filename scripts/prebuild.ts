/**
 * Prebuild Script
 *
 * The changelog page (content/docs/<lang>/guide/wiki/changelog.mdx) was removed
 * together with the rest of the "Introduction" group, so changelog generation is
 * no longer run here. Kept as an extension point for future prebuild steps.
 */

async function prebuild() {
  console.log('═══════════════════════════════════════════════');
  console.log('🚀 Prebuild: nothing to do.');
  console.log('═══════════════════════════════════════════════\n');
}

// Execute prebuild
prebuild();
