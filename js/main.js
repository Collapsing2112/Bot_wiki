// 初始化Marked
marked.setOptions({
    highlight: function(code, lang) {
        return hljs.highlightAuto(code).value;
    }
});

// 加载文章列表
async function loadArticles() {
    const response = await fetch('articles/list.json');
    const articles = await response.json();
    
    // 生成侧边栏导航
    const sidebar = document.getElementById('sidebar');
    articles.forEach(article => {
        const link = document.createElement('a');
        link.href = `#${article.id}`;
        link.textContent = article.title;
        link.onclick = () => loadArticle(article.file);
        sidebar.appendChild(link);
    });

    // 默认加载第一篇文章
    if(articles.length > 0) loadArticle(articles[0].file);
}

// 加载单篇文章
async function loadArticle(filename) {
    const response = await fetch(`articles/${filename}`);
    const mdContent = await response.text();
    document.getElementById('content').innerHTML = marked.parse(mdContent);
}

// 初始化
document.addEventListener('DOMContentLoaded', loadArticles);