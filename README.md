**Demo [[針對一般用戶]](https://youtu.be/bsRU4NSQtYA) / [[針對新使用者]](https://youtu.be/aTQcOmel8l0)**
### Intro
大家或許都有過這樣的體驗：三五好友說好要一起度過一個電影之夜，準備好了爆米花，卻因為選擇障礙，在沙發上坐了 20 分鐘還是不知道要看什麼；又或是隨意選了一部不對胃口的電影，白白花了兩個小時，既沒得到原本期待的收穫，好心情也因此變得沮喪。所以，幫我們將數以萬計的選擇縮小到個位數—這就是推薦系統的重要。 
 
有鑑於此，本研究計畫欲結合臉部辨識和機器學習技術建構出一個創新的推薦系統，包含完善的電影檢索、查詢和記錄功能，設計出一款電影推薦平台app，並裝載於台灣 ASUS 開發的 Zenbo 居家機器人，不僅能依前置鏡頭快速的辨識出使用者身分、情緒，還能藉資料庫的連結記下使用者的喜好，調出觀看紀錄和做出最個人化、根據使用者狀況的推薦，幫助不論是一個家庭、三五好友，或任何喜愛電影的使用者，在適當的時機看一部最適合的電影，讓電影的效用發揮到最大。
 
### Motive
* **電影不再只是休閒時間的娛樂，更是補給心靈的一帖良藥：**

在心理學上有專業的「電影療法」，藉找到能與自身遭遇產生強烈	共鳴的影片，因而受到啟發、深化自我意識，從而改變自身困境。	若而若在剛好的時機看一部對的電影，就能為情緒找到出口，那能	不能有一個自動、且更人性化的電影推薦系統？

* **推薦系統能做的或許更多：**

除了根據使用者當下的狀況判斷，更藉由長期的觀察和紀錄幫助使	用者找出「自己的偏好」。

* **市面上沒有一個專門的推薦系統：**

電影系統大都附加於串流平台上，要是我今天只是想隨意找一部電	影來看？只是想好好記下所有自己看過的電影？


---

### Implementation
![](https://i.imgur.com/38gRnoa.png)

**1 個人化推薦：**

選擇以Keras 實作Bayesian Personalized Ranking，相較於基本推薦模型 Matrix Factorization，它更著重於用戶對於物品A與物品B之間可能喜好程度的比較，使得推薦出來的結果排序更個人化。

**2 情緒推薦**

由於情緒對於電影之資料集的不足，難以用模型訓練，於是我們查閱了「電影療法」相關的研究，並以rule base根據label推薦。

**3 相關推薦：**

利用Word2Vec，把資料集中用戶前後看過的電影當成字串做處理，藉此找出「看過這個電影的人，還看過…」為相關電影之推薦。

**4 對電影之基本操作：**

對電影的操作不只可以幫助使用者紀錄，也是開發者訓練推薦模型的重要資料來源。使用者所有點過、評分、收藏之電影皆會從前端發request到後端存進MySQL資料庫。


---

### Program Strcture
![](https://i.imgur.com/3Gbx3vx.png)

#### Front End：
考慮到完成時間及呈現出之效果，我們採用hybrid app的技術。
利用Android Camera2實現簡單觸屏拍照功能，包含點擊後短暫的預覽，隨即以AsyncTask利用HTTP Request方式傳送資料給後端。
收到後端傳回之辨識結果後，開啟WebView。而在製作網頁中運用到了Sass、Pug等preprocessor；電影資訊來自Tmdb所提供之api，並在呈現上利用d3.js來增添畫面的多樣性。

#### Back End：
後端選擇使用Django作為框架。   
臉部辨識部分考量其效益和即時性，在實作後改選擇使用Azure FaceAPI，而後端負責之其他工作包含以Keras實現之推薦模型、與MySQL資料庫之互動和各式資料處理。



---

### Screenshot
* 拍照辨識畫面

![](https://i.imgur.com/69n29nX.jpg)

* 推薦主頁面

![](https://i.imgur.com/p0hP27H.jpg)

* 電影資訊及相關電影推薦

![](https://i.imgur.com/afO8dWZ.jpg)


