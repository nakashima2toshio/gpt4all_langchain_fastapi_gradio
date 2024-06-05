### Fine Tuning by Hugging Face - Transformer and PyTorch

- [テキスト分類のデータセット]で[モデルをファインチューニング]する一般的なタスク
- from_pretrained()を用いてモデルをインスタンス化
- 「TF」で始まらない「Huggingface Transformers」のモデルクラスはPyTorchモジュールです。
- 推論と最適化の両方でPyTorchのモデルと同じように利用できます。
  - 初期化
    - 「モデル構成」
    - 「事前学習した重み」
    - ランダムにインスタンス化される重みを持つタスク固有の「最終層」または「ヘッド」も多数含まれています。
      - 最終層
      - ヘッド
        ```python:
        from transformers import BertForSequenceClassification
        
        model = BertForSequenceClassification.from_pretrained('bert-base-uncased', return_dict=True)
        model.train() # 訓練モードに変更
        ```
      - 「bert-base-uncased」モデルからコピーされたエンコーダ
      - 「重み」と、「出力サイズ2のエンコーダ」の上にある「ランダムに初期化」された
      - 「テキスト分類ヘッド」を持つ 
      - モデルのインスタンスが作成されます。
      - モデルは、デフォルトでは「評価モード」で初期化
      - model.train() を呼び出すことで、「訓練モード」
      - 事前学習したBERTエンコーダを利用して、任意のテキスト分類のデータセットで簡単に学習できるので便利
      - ライブラリには、「重み減衰」と同様に「勾配バイアス補正」を実装したAdamWオプティマイザも用
      - 
