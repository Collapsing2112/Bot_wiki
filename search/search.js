let searchIndex = null;

// 初始化搜索索引
async function initSearch() {
    const response = await fetch('articles/list.json');
    const articles = await response.json();
    
    searchIndex = lunr(function() {
        this.ref('id');
        this.field('title');
        this.field('content');
        
        articles.forEach(article => {
            this.add({
                id: article.id,
                title: article.title,
                content: article.contentPreview
            });
        });
    });
}

// 执行搜索
document.getElementById('searchInput').addEventListener('input', function(e) {
    const results = searchIndex.search(e.target.value);
    const resultsContainer = document.getElementById('searchResults');
    
    resultsContainer.innerHTML = results
        .map(result => `<a href="#${result.ref}">${result.matchData.metadata.title}</a>`)
        .join('');
});

// 初始化搜索
document.addEventListener('DOMContentLoaded', initSearch);