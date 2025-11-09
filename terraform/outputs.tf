output "alb_dns_name" {
  value = aws_lb.public.dns_name
}

output "cluster_name" {
  value = aws_ecs_cluster.main.name
}
