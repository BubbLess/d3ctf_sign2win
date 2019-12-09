# 题目部署

可使用docker部署，在本目录下运行

>docker build -t 'sign2win' .
>
>Docker run -d -p '0.0.0.0:12233:12233' -h "sign2win" --name="sign2win" sign2win