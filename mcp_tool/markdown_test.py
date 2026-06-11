# markitdown example.pdf -o example.md
# markitdown /Users/twinb00551192/Desktop/AItest/總覽20260113.xlsx  -o output.md
# which ffmpeg 或 ffmpeg -version
import pandas as pd
from pathlib import Path



def multiline_to_md_list(text):
    if pd.isna(text):
        return ""

    lines = str(text).splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    # 轉成 markdown list（用 <br> 避免表格破版）
    return "<br>".join(f"- {line}" for line in lines)


def filter_content(file_name):
    file_path = Path(__file__).resolve().parents[1].joinpath('data', 'case', f'20260113.xlsx')
    df = pd.read_excel(file_path)
    filter_df = df[['測試案例','功能大類','功能名稱','前置條件','測試步驟','預期結果','備註']].copy()

    # 將多行文字轉換為 markdown 列表格式
    multiline_cols = ['前置條件', '測試步驟', '預期結果','備註']
    for col in multiline_cols:
        filter_df[col] = filter_df[col].apply(multiline_to_md_list)

    output_path = Path(__file__).resolve().parents[1].joinpath('data', 'case_md', f'{file_name}.md')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    md_text = filter_df.to_markdown(index=False)
    output_path.write_text(md_text, encoding='utf-8')

if __name__ == "__main__":
    filter_content('testcase_2')
