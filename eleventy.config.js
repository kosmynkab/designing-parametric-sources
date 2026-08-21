export default function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ "src/imgs": "imgs" });
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addWatchTarget("./src/_data/projects");
  eleventyConfig.addCollection("siteNavigation", (collectionApi) => {
    return collectionApi
      .getAll()
      .filter((item) => item.data.navigation)
      .sort((first, second) => {
        return (
          (first.data.navigation.order || 0) -
          (second.data.navigation.order || 0)
        );
      });
  });
  
  return {
    pathPrefix: process.env.ELEVENTY_PATH_PREFIX || "/",
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes"
    }
  };
}