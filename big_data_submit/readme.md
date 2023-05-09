  

<div style="text-align: center">

    <span style="font-size: 3em; font-weight: 700; font-family: Consolas">

        Lab 03  <br>

		Community Detection
		
    </span>

    <br><br>

    <span style="">

        A assignment for <code>CSC14114</code>  Big Data Application @ 19KHMT

    </span>

</div>

  
  

## Collaborators (nhom 1)

- `19127519` **Nguyễn Ngọc Phước** ([Nguyễn Ngọc Phước](https://github.com/SilentCatD))

- `19127523` **Đặng Nguyễn Minh Quân** ([Đặng Nguyễn Minh Quân](https://github.com/quainhan1110))

## Instructors

- `HCMUS` **Đoàn Đình Toàn** ([@ddtoan](ddtoan18@clc.fitus.edu.vn))

- `HCMUS` **Nguyễn Ngọc Thảo** ([@nnthao](nnthao@fit.hcmus.edu.vn))

---

<div style="page-break-after: always"></div>
## How to run my code

- Just run the `main.py` file. It's that simple ;).
- Do note that the source code may require additional library to be installed, I use `pip` to install them, and have perform `pip freeze > requirements.txt`. You may have to run `pip install -r requirements.txt` first to get all nessessary library/pacakges.
- In the source code, I use only :
	- `pandas`: to process csv file
	- `tdqm`: to show progressbar
	- `networkx`: to do comparision with self-implemmented algorithms.
- In my implemmentation, I have use many patterns and ways to perform assigned task:
	- Apply `Builder` design pattern to construct different graphs
	- Apply `Template method` design pattern to perform edge betweenness calculations and community detection (there's an interfaces that different kind of implemmentations implemented on)
	- `Edge Betweenness` calculation is done via `Tree` data structure, and calculation is performed in `recursive` manner, I'm quite proud of this.
	- All my code is self implemmented.f
- This lab is harder than the others 2.
